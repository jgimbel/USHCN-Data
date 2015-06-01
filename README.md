# USHCN-Data#
##Finding the average amount of precipitation per day##

###Setting up a virtual box###
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
The data is formatted with a entire month worth of data in one record.
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

    hive
    hive> CREATE TABLE PRCP (value INT, date STRING, measurement STRING, quality STRING, source STRING) 
        > ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';
        
    hive> LOAD DATA LOCAL INPATH 'PRCP.csv' INTO TABLE prcp; 

This is helpful in loading data, but not necessarily the smallest way to store data.  To help store the data in smaller amount lets convert our csv file into an ORC file.

    hive> CREATE TABLE PRECEP (value INT, date STRING, measurement STRING, quality STRING, source STRING) 
        > STORED AS orc;
    hive> INSERT INTO TABLE precep SELECT * from prcp;
    
