## 设置时区
sudo cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

## 安装mongodb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 4B7C549A058F8B6B
# echo "deb [ arch=amd64 ] https://mirrors.tuna.tsinghua.edu.cn/mongodb/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl enable mongod
sudo service mongod restart
sudo apt-get install -y python3-pymongo
ps -ef | grep 'mongod' | grep -v grep | awk '{print $2}' | sudo xargs sudo kill -9
sudo mongod --fork --dbpath /var/lib/mongodb/ --bind_ip 127.0.0.1 --port 27117

## 安装redis
sudo apt-get -y install redis-server
sudo sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf
sudo sed -i 's/# requirepass foobared/requirepass gtcA4010/g' /etc/redis/redis.conf
sudo service redis-server restart

## pip包的安装
sudo apt-get install -yqq python3-distutils python3-pip
pip3 install --upgrade pip setuptools

pip3 install flask scrapy beautifulsoup4 dnspython gunicorn supervisor numpy

pip3 install shapely geopandas matplotlib redis Python-EasyGraph networkx seaborn

## 安装apt
sudo apt-get -yqq install wondershaper nload iftop zip unzip htop jq msttcorefonts
rm ~/.cache/matplotlib -rf

## 安装iperf3
cd ~
sudo apt -y remove iperf3 libiperf0 
sudo apt -y install libsctp1 
wget https://iperf.fr/download/ubuntu/libiperf0_3.7-3_amd64.deb 
wget https://iperf.fr/download/ubuntu/iperf3_3.7-3_amd64.deb 
sudo dpkg -i li3biperf0_3.7-3_amd64.deb iperf3_3.7-3_amd64.deb

## 安装mininet
sudo rm -rf /usr/bin/python
sudo ln -s /usr/bin/python3.6 /usr/bin/python
cd ~
git clone https://github.com/mininet/mininet.git
cd ~/mininet
util/install.sh -nv

## 语言环境 
echo "export PYTHONIOENCONDING=utf8" >> ~/.zshrc 
echo "export LC_ALL=en_US.UTF-8" >> ~/.zshrc 
echo "export LANG=en_US.UTF-8" >> ~/.zshrc 
echo "export PYTHONWARNINGS=ignore" >> ~/.zshrc 
echo "export PYTHONPATH=$PYTHONPATH:$HOME/mininet" >> ~/.zshrc 
source ~/.zshrc

# 目录权限管理
sudo chown -R gtc:socnet-PG0 ~/.config

## 设置进程限制
echo 530603 | sudo tee /sys/fs/cgroup/pids/user.slice/user-${UID}.slice/pids.max 
sudo sed -i 's/#UserTasksMax=33%/UserTasksMax=infinity/g' /etc/systemd/logind.conf
sudo sed -i 's/#DefaultTasksAccounting=yes/DefaultTasksAccounting=no/g' /etc/systemd/system.conf
echo "root            soft    nproc           330603" | sudo tee -a /etc/security/limits.conf
echo "root            hard    nproc           330603" | sudo tee -a /etc/security/limits.conf
echo "root            soft    nofile          102400" | sudo tee -a /etc/security/limits.conf
echo "root            hard    nofile          102400" | sudo tee -a /etc/security/limits.conf
echo "gtc            soft    nproc           330603" | sudo tee -a /etc/security/limits.conf
echo "gtc            hard    nproc           330603" | sudo tee -a /etc/security/limits.conf
echo "gtc            soft    nofile          102400" | sudo tee -a /etc/security/limits.conf
echo "gtc            hard    nofile          102400" | sudo tee -a /etc/security/limits.conf

# ## cache相关
# deb http://us.archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse
# deb-src http://us.archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse
# sudo apt-get update
# sudo apt-get install -yqq libglib2.0-dev python3-pip python3-matplotlib
# pip3 install heapdict mmh3 PyMimircache
# git clone -b master --recurse-submodules git@github.com:1a1a11a/PyMimircache.git
# cd PyMimircache
# sudo python3 setup.py install

## Matlab字体
## 缺少字体：https://stackoverflow.com/questions/42097053/matplotlib-cannot-find-basic-fonts
## 中文字体：https://blog.csdn.net/weixin_45772050/article/details/121222052

# Install Docker
wget -qO- https://get.docker.com/ | sh
