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

