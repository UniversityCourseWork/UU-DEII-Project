#!/bin/bash

# Check for root access
if [[ $EUID -ne 0 ]];
then
    # Rerun the script with elevated priviledge
    exec sudo /bin/bash "$0" "$@";

    exit "$?";
fi

# Skipping the annoying prompts of kernel restart
export NEEDRESTART_MODE=a
sed -i "s/#\$nrconf{kernelhints} = -1;/\$nrconf{kernelhints} = -1;/g" /etc/needrestart/needrestart.conf

# Perform updates and upgrade
apt update; apt -y upgrade

# Install required tools and dependencies
apt -y install curl tmux 

# Install pip3 package manager and virtual environment
apt -y install python3 python3-pip python3-venv

# Install Openstack components
add-apt-repository cloud-archive:yoga
apt -y install nova-compute

# Install API related packages
apt -y install python3-openstackclient python3-novaclient python3-keystoneclient

# Install dependencies
python3 -m pip install -r requirements.txt

# Perform updates and upgrade
apt update; apt -y upgrade
