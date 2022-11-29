FROM ubuntu:20.04

COPY ./ /root/socialcache

# apt install packages
RUN apt-get update && \
    apt-get install -yqq wondershaper nload iftop zip unzip htop jq python3.8 && \
    apt-get -y install apt-utils redis-server && \
    sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf && \
    sed -i 's/# requirepass foobared/requirepass gtcA4010/g' /etc/redis/redis.conf && \
    service redis-server restart

## 安装iperf3
RUN cd ~ && \
    apt -y remove iperf3 libiperf0 && \
    apt -y install libsctp1 wget iperf3

## 安装mininet
RUN apt-get install -yqq git sudo systemctl && \
    cd ~ && git clone https://github.com/mininet/mininet.git && \
    sudo ./mininet/util/install.sh -nv

## 语言环境 
RUN echo "export PYTHONIOENCONDING=utf8" >> ~/.bashrc && \
    echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc && \
    echo "export LANG=en_US.UTF-8" >> ~/.bashrc && \
    echo "export PYTHONWARNINGS=ignore" >> ~/.bashrc && \
    echo "export PYTHONPATH=$PYTHONPATH:$HOME/mininet" >> ~/.bashrc
#    source ~/.bashrc

# install pip packages
RUN apt-get install -yqq python3-distutils python3-pip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install flask scrapy beautifulsoup4 dnspython gunicorn supervisor numpy && \
    pip3 install geos shapely geopandas matplotlib redis Python-EasyGraph networkx seaborn
