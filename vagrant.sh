#!/usr/bin/env bash

# add swap
fallocate -l 4G /swapfile && chmod 0600 /swapfile && mkswap /swapfile && swapon /swapfile && echo '/swapfile none swap sw 0 0' >> /etc/fstab
echo vm.swappiness = 10 >> /etc/sysctl.conf && echo vm.vfs_cache_pressure = 50 >> /etc/sysctl.conf && sysctl -p


# use local ubuntu mirror  
sed -i 's/archive.ubuntu.com/lv.archive.ubuntu.com/g' /etc/apt/sources.list

# update apt-get
sudo apt-get update

# install various dependencies
sudo apt-get -y install build-essential libreadline-gplv2-dev libncursesw5-dev \
	libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev sshpass \
	git-core sloccount


# Install Python3.6 & PIP
sudo apt-get -y install python3.6 python-pip python-dev libpq-dev
sudo pip install --upgrade pip
# @see https://pip.pypa.io/en/latest/reference/pip.html

# Install projects Requirements
sudo pip install -qq -r /requirements.txt


# Setup Python Config
APP_SETTINGS="config.ProductionConfig"
export APP_SETTINGS


# Install SQLite3
sudo apt-get -y install sqlite3 libsqlite3-dev

# create folder for SQLite DB
cd /tmp
mkdir tmp
sudo chown www-data:www-data /tmp/tmp

# create DB tables, set folder and file permissions
cd /var/www/
python db_create_users.py
python db_create_posts.py
sudo chown www-data:www-data /tmp/tmp/sample.db
sudo chmod -R 777 /tmp/tmp



# Open port 80
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables-save

