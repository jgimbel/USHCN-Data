# USHCN-Data
##Finding the average amount of precipitation per day

###Setting up a virtual box
First install virtualbox

In Arch Linux

    sudo pacman -S virtualbox
    sudo modprobe vboxdrv #add Virtualbox to the kernel
In debian/Ubuntu

    sudo apt-get install virtualbox 
In SUSE/REHL/CentOS

    wget http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo > /etc/yum.d/virtualbox.repo
    yum update
    rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm  #Dependencies
    yum install binutils gcc make patch libgomp glibc-headers glibc-devel kernel-headers kernel-devel dkms
    yum install VirtualBox-4.3
    service vboxdrv setup

Then download a sandbox from HortonWorks

    wget http://hortonassets.s3.amazonaws.com/2.2.4/Sandbox_HDP_2.2.4.2_VirtualBox.ova
Once the virtual drive has been downloaded, open it with virtualbox

    VirtualBox Sandbox_HDP_2.2.4.1_VirtualBox.ova
Now simply ssh into the virtualbox

    ssh -p 2222 root@localhost
    
###Loading data into Hive###
First download and decompress the gzip file

    wget http://cdiac.ornl.gov/ftp/ushcn_daily/state25_NE.txt.gz
    gzip -d state25_NE.txt.gz
Then we need to format the data to import it into Hive.
The data is formatted with an entire month worth of data in one record.
To help understand each row, this is the json equivalent:

    {
      COOPID: String,
      YEAR: Integer,
      MONTH: Integer,
      ELEMENT: String,
      VALUES: [{
        VALUE: Integer,
        MFLAF: Character,
        QFLAG: Character,
        SFLAG: Character
      }]
    }
I wrote a python script to convert the file to json.

    ./txtToJson.py
This script requires a lot of memory because it must store all records before it writes them to the file. It also creates a very large file. Because of this I chose to create csv files instead.  This format did not require more RAM because I could write each line to the file and then remove the line from memory. This caused the program to run slower because it was doing file IO each loop (Even on a SSD). I created one file per ELEMENT type because it is easier to do a join than to query over mismatched data.  This also removed excess data, such as if I do not need SNOW related data, I would be able to discard that file.

To run this csv script simply...

    ./state.py

Once this is created I imported each file by running Hive's CLI, creating each database, and importing the data

    $ hive
    hive> CREATE TABLE PRCP (value INT, date STRING, measurement STRING, quality STRING, source STRING) 
        > ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
        
    hive> LOAD DATA LOCAL INPATH 'PRCP.csv' INTO TABLE prcp; 

This is helpful in loading data, but not necessarily the smallest way to store data.  To help store the data in smaller amount lets convert our csv file into an ORC file.

    hive> CREATE TABLE PRECEP (value INT, date STRING, measurement STRING, quality STRING, source STRING) 
        > STORED AS orc;
    hive> INSERT INTO TABLE precep SELECT * from prcp;
    
I grabbed the warehouse out of hdfs to check how much ORC compressed that one file.  Turns out to be quite a lot.  The original csv file is 32MB large. The compressed orc system is a total of 5MB, so about 1/6 the size.

###Running SQL queries###

To start we must understand our problem.  Nebraska is large, and so there are many weather stations and groups that measure the amount of water it gets.  To get a good estimate for each day it rained an average can be taken. This means grouping our values by the date, then taking the average of those values.  In SQL this this is done like

    SELECT date, avg(value) FROM prcp WHERE date like '%-12-22' GROUP BY date ORDER BY date;
Luckily for us this translates to HiveQL exactly, so no changes are needed to run that from the CLI

To run this on spark we must simply import the HiveContext and run our sql queries

    $ pyspark
    >>> from pyspark.sql import HiveContext
    >>> cxt = HiveContext(sc)  #sc is your sparkContext, create for you when pyspark starts
    >>> result = cxt.sql("SELECT date, avg(value) as average \
                          FROM prcp \
                          WHERE date like '%-12-22' \
                          GROUP BY date ORDER BY date")
    >>> for row in result.collect():
    ....    print(row.date.split('-')[0], row.average)
    ....
    <A very nice output goes here>
    >>>exit()
Or if you have pyspark in your PYTHONPATH, just run the script in this repo

    $ ./SparkHiveQuery.py
    
To add pyspark to your PYTHONPATH use this export

    $ export PYTHONPATH=/usr/hdp/current/spark-client/python
    $ export SPARK_HOME=/usr/hdp/current/spark-client
The important question that still remains is how did converting to orc change our query?  From running the same query on both th csv file and the ORC file, they both ran at about 20 seconds per query, with csv having just Milliseconds faster time.
