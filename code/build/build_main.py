import mininet
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info, warning
from mininet.link import TCLink, Intf
import copy
import json
import time
import os
import subprocess
import sys
import configparser
import code.util.simple_httpserver as simple_httpserver

# SELECT_TOPO = json.load(open('../json-files/topo.json', 'r'))

class Build_network:
    def __init__(self):
        '''首先删除上一次拓扑'''
        ret = subprocess.Popen("sudo mn -c", shell=True,stdout=subprocess.PIPE)
        data=ret.communicate() 
        ret.wait() 

        ''' 初始化节点列表 '''
        self.level_1_host = []
        self.level_2_host = []
        self.level_3_host = []
        self.user_host = []

        self.switch = []

        '''读取topo文件，并设置参数'''
        self.topo = json.load(open('code/build/topo.json', 'r'))
        self.level_1_host_number = len(self.topo['level_1_id'])
        self.level_2_host_number = len(self.topo['level_2_id'])
        self.level_3_host_number = len(self.topo['level_3_id'])
        self.user_host_number = len(self.topo['user_id'])

        self.level_1_host_ip = ['' for _ in range(self.level_1_host_number)]
        self.level_2_host_ip = ['' for _ in range(self.level_2_host_number)]
        self.level_3_host_ip = ['' for _ in range(self.level_3_host_number)]
        self.user_host_ip = ['' for _ in range(self.user_host_number)]

        self.switch_number = self.level_1_host_number + self.level_2_host_number + self.user_host_number + 1  #设置switch数量，除了最下面一层，每层各有一个switch; 每个user各有一个switch，最后一个用来帮助redis连外网

        '''获得本机的IP地址，作为redis_ip，并获得redis_ip的前缀'''
        # self.redis_ip = "128.105.145.13"
        ret = subprocess.Popen("ifconfig eno1 | grep inet | awk '{print $2}' | cut -f 2 -d ':'",shell=True,stdout=subprocess.PIPE)
        self.redis_ip = ret.stdout.read().decode("utf-8").strip('\n')
        ret.stdout.close()

        self.redis_ip_subnet = str(self.redis_ip.split('.')[0]) + '.' + \
                                str(self.redis_ip.split('.')[1]) + '.' + \
                                str(self.redis_ip.split('.')[2]) + '.0' + '/24'

        self.net = Mininet( topo=None,
            build=False,
            host=CPULimitedHost,
            ipBase='10.0.0.0/8',
            controller=None,
            waitConnected=True)
            
    def myNetwork(self):
        '''
            Node name: first character from 'a' to 'c', means level 1 to level 3; second character from 0 to n;
            IP address: for xth cache in y level, the IP address will be 10.0.x.(y*2-1)
        '''

        setLogLevel( 'warning' )

        '''将第二个网卡配置清空，为了方便之后重新配置，协助mininet内部节点连接本机'''
        os.system('ifconfig eno2 0')

        print('*** Add switches\n')
        for switch_id in range(self.switch_number):
            self.switch.append(self.net.addSwitch('sw%s'%str(switch_id), cls=OVSKernelSwitch, failMode='standalone', stp=True)) ## 防止回路
        
        '''在添加后需要立刻将switch启动一次，以防超过连接数后被吞网关'''
        for switch_id in range(self.switch_number):
            self.net.get('sw%s'%str(switch_id)).start([])
        
        '''定义网卡'''
        for switch_id in range(self.switch_number):
            self.switch[switch_id].cmd('sysctl -w net.ipv4.ip_forward=1')

        '''将最后1个switch和网卡eno2相连，并获取网关地址'''
        print("sudo ifconfig sw%s 10.0.%s.15/24"%(str(self.switch_number-1), str(100)))
        ret = subprocess.Popen("sudo ifconfig sw%s 10.0.%s.15/24"%(str(self.switch_number-1), str(100)), shell=True,stdout=subprocess.PIPE)
        data=ret.communicate() 
        ret.wait() 

        print('*** Post configure switches and hosts\n')

        time.sleep(5)

        switch_gw = [0 for _ in range(3)]
        switch_gw_pre3 = [0 for _ in range(3)]
        ret = subprocess.Popen("ifconfig sw%s | grep inet | awk '{print $2}' | cut -f 2 -d ':'"%(str(self.switch_number-1)),shell=True,stdout=subprocess.PIPE)
        data=ret.communicate()
        ret.wait()

        switch_gw = data[0].decode("utf-8").strip('\n')
        print("switch_gw: ", switch_gw)
        switch_gw_pre3 = str(switch_gw.split('.')[0]) + '.' + \
                            str(switch_gw.split('.')[1]) + '.' + \
                            str(switch_gw.split('.')[2])
        print("switch_gw_pre3: ", switch_gw_pre3)

        print('*** Add hosts\n')
        for level_1_host_id in range(self.level_1_host_number):
            self.level_1_host_ip[level_1_host_id] = '10.0.%s.1'%str(level_1_host_id)
            self.level_1_host.append(self.net.addHost('a%s'%str(level_1_host_id), cpu=self.topo['cpu_level_1']/self.level_1_host_number, ip=self.level_1_host_ip[level_1_host_id], defaultRoute=None)) 
        for level_2_host_id in range(self.level_2_host_number):
            self.level_2_host_ip[level_2_host_id] = '10.0.%s.3'%str(level_2_host_id)
            self.level_2_host.append(self.net.addHost('b%s'%str(level_2_host_id), cpu=self.topo['cpu_level_2']/self.level_2_host_number, ip=self.level_2_host_ip[level_2_host_id], defaultRoute=None)) 
        for level_3_host_id in range(self.level_3_host_number):
            self.level_3_host_ip[level_3_host_id] = '10.0.%s.5'%str(level_3_host_id)
            self.level_3_host.append(self.net.addHost('c%s'%str(level_3_host_id), cpu=self.topo['cpu_level_3']/self.level_3_host_number, ip=self.level_3_host_ip[level_3_host_id], defaultRoute=None)) 
        '''建立一个user节点，这样才能使用wget获取mininet内部的数据'''
        for user_host_id in range(self.user_host_number):
            self.user_host_ip[user_host_id] = '10.0.%s.10'%str(user_host_id)
            self.user_host.append(self.net.addHost('u%s'%str(user_host_id), cpu=self.topo['cpu_user']/self.user_host_number, ip=self.user_host_ip[user_host_id], defaultRoute=None)) 
        
        print('*** Add links\n')
        '''level_1和level_2之间的结果，通过level_1对应的switch相连'''
        for level_1_host_id in range(self.level_1_host_number):
            for level_2_host_id in range(self.level_2_host_number):
                self.net.addLink(self.switch[level_1_host_id], self.level_2_host[level_2_host_id], cls=TCLink, **{'bw':self.topo['bandwidth_topo'][self.topo['level_1_id'][level_1_host_id]][self.topo['level_2_id'][level_2_host_id]],'delay':str(self.topo['delay_topo'][self.topo['level_1_id'][level_1_host_id]][self.topo['level_2_id'][level_2_host_id]])+'ms', 'max_queue_size':1000, 'loss':0, 'use_htb':True})
            self.net.addLink(self.switch[level_1_host_id], self.level_1_host[level_1_host_id], cls=None)

        '''level_2和level_3之间的结果，通过level_2对应的switch相连'''
        for level_2_host_id in range(self.level_2_host_number):
            for level_3_host_id in range(self.level_3_host_number):
                self.net.addLink(self.switch[self.level_1_host_number + level_2_host_id], self.level_3_host[level_3_host_id], cls=TCLink, **{'bw':self.topo['bandwidth_topo'][self.topo['level_2_id'][level_2_host_id]][self.topo['level_3_id'][level_3_host_id]],'delay':str(self.topo['delay_topo'][self.topo['level_2_id'][level_2_host_id]][self.topo['level_3_id'][level_3_host_id]])+'ms', 'max_queue_size':1000, 'loss':0, 'use_htb':True})
            self.net.addLink(self.switch[self.level_1_host_number + level_2_host_id], self.level_2_host[level_2_host_id], cls=None)
        
        '''将所有节点和所有user对应的switch相连，连接user'''
        for user_host_id in range(self.user_host_number):
            curr_switch_id = self.level_1_host_number + self.level_2_host_number + user_host_id
            for level_1_host_id in range(self.level_1_host_number):
                self.net.addLink(self.switch[curr_switch_id], self.level_1_host[level_1_host_id], cls=TCLink, **{'bw':self.topo['bandwidth_topo'][self.topo['user_id'][user_host_id]][self.topo['level_1_id'][level_1_host_id]],'delay':str(self.topo['delay_topo'][self.topo['user_id'][user_host_id]][self.topo['level_1_id'][level_1_host_id]])+'ms', 'max_queue_size':1000, 'loss':0, 'use_htb':True})
            for level_2_host_id in range(self.level_2_host_number):
                self.net.addLink(self.switch[curr_switch_id], self.level_2_host[level_2_host_id], cls=TCLink, **{'bw':self.topo['bandwidth_topo'][self.topo['user_id'][user_host_id]][self.topo['level_2_id'][level_2_host_id]],'delay':str(self.topo['delay_topo'][self.topo['user_id'][user_host_id]][self.topo['level_2_id'][level_2_host_id]])+'ms', 'max_queue_size':1000, 'loss':0, 'use_htb':True})
            for level_3_host_id in range(self.level_3_host_number):
                self.net.addLink(self.switch[curr_switch_id], self.level_3_host[level_3_host_id], cls=TCLink, **{'bw':self.topo['bandwidth_topo'][self.topo['user_id'][user_host_id]][self.topo['level_3_id'][level_3_host_id]],'delay':str(self.topo['delay_topo'][self.topo['user_id'][user_host_id]][self.topo['level_3_id'][level_3_host_id]])+'ms', 'max_queue_size':1000, 'loss':0, 'use_htb':True})  
            self.net.addLink(self.switch[curr_switch_id], self.user_host[user_host_id], cls=None)

        '''将节点和外网，通过最后一个switch相连'''
        for level_1_host_id in range(self.level_1_host_number):
            self.net.addLink(self.switch[self.switch_number-1], self.level_1_host[level_1_host_id], cls=None)
        for level_2_host_id in range(self.level_2_host_number):
            self.net.addLink(self.switch[self.switch_number-1], self.level_2_host[level_2_host_id], cls=None)
        for level_3_host_id in range(self.level_3_host_number):
            self.net.addLink(self.switch[self.switch_number-1], self.level_3_host[level_3_host_id], cls=None)
        for user_host_id in range(self.user_host_number):
            self.net.addLink(self.switch[self.switch_number-1], self.user_host[user_host_id], cls=None)
        
        print('*** Config Networks\n')

        '''对具体的网卡指定对应的ip'''
        for level_1_host_id in range(self.level_1_host_number):
            self.level_1_host[level_1_host_id].cmdPrint('ifconfig a%s-eth%s 0'%(str(level_1_host_id), str(0))) ## eth0和自己的switch相连
            self.level_1_host[level_1_host_id].cmdPrint('ifconfig a%s-eth%s %s.%s/24'%(str(level_1_host_id), str(self.user_host_number+1), str(switch_gw_pre3), str(100+level_1_host_id))) ## 连接外网

        for level_2_host_id in range(self.level_2_host_number):
            self.level_2_host[level_2_host_id].cmdPrint('ifconfig b%s-eth%s 0'%(str(level_2_host_id), str(self.level_1_host_number))) ## eth0--eth{level_1_host_number-1}和level_1的节点相连，下一个和自己的switch相连。
            self.level_2_host[level_2_host_id].cmdPrint('ifconfig b%s-eth%s %s.%s/24'%(str(level_2_host_id), str(self.level_1_host_number+self.user_host_number+1), str(switch_gw_pre3), str(125+level_2_host_id))) ## 连接外网

        for level_3_host_id in range(self.level_3_host_number):
            self.level_3_host[level_3_host_id].cmdPrint('ifconfig c%s-eth%s %s.%s/24'%(str(level_3_host_id), str(self.level_2_host_number+self.user_host_number), str(switch_gw_pre3), str(150+level_3_host_id))) ## 连接外网

        for user_host_id in range(self.user_host_number):
            self.user_host[user_host_id].cmdPrint('ifconfig u%s-eth%s 0'%(str(user_host_id), str(0))) ## eth0和自己的switch相连
            self.user_host[user_host_id].cmdPrint('ifconfig u%s-eth%s %s.%s/24'%(str(user_host_id), str(1), str(switch_gw_pre3), str(175+user_host_id))) ## 连接外网
        
        '''配置路由表'''
        '''level_1发出'''
        for level_1_host_id in range(self.level_1_host_number):
            for level_2_host_id in range(self.level_2_host_number):
                self.level_1_host[level_1_host_id].cmdPrint("route add -host 10.0.%s.3 dev a%s-eth%s" %(str(level_2_host_id), str(level_1_host_id), str(0)))
            for user_host_id in range(self.user_host_number):
                self.level_1_host[level_1_host_id].cmdPrint("route add -host 10.0.%s.10 dev a%s-eth%s" %(str(user_host_id), str(level_1_host_id), str(1+user_host_id)))
            self.level_1_host[level_1_host_id].cmdPrint("route add -net %s gw %s"%(str(self.redis_ip_subnet), str(switch_gw)))  

        '''level_2发出'''
        for level_2_host_id in range(self.level_2_host_number):
            for level_1_host_id in range(self.level_1_host_number):
                self.level_2_host[level_2_host_id].cmdPrint("route add -host 10.0.%s.1 dev b%s-eth%s" %(str(level_1_host_id), str(level_2_host_id), str(level_1_host_id)))
            for level_3_host_id in range(self.level_3_host_number):
                self.level_2_host[level_2_host_id].cmdPrint("route add -host 10.0.%s.5 dev b%s-eth%s" %(str(level_3_host_id), str(level_2_host_id), str(self.level_1_host_number)))
            for user_host_id in range(self.user_host_number):
                self.level_2_host[level_2_host_id].cmdPrint("route add -host 10.0.%s.10 dev b%s-eth%s" %(str(user_host_id), str(level_2_host_id), str(self.level_1_host_number+user_host_id+1)))
            self.level_2_host[level_2_host_id].cmdPrint("route add -net %s gw %s"%(str(self.redis_ip_subnet), str(switch_gw)))  

        '''level_3发出'''
        for level_3_host_id in range(self.level_3_host_number):
            for level_2_host_id in range(self.level_2_host_number):
                self.level_3_host[level_3_host_id].cmdPrint("route add -host 10.0.%s.3 dev c%s-eth%s" %(str(level_2_host_id), str(level_3_host_id), str(level_2_host_id)))
            for user_host_id in range(self.user_host_number):
                self.level_3_host[level_3_host_id].cmdPrint("route add -host 10.0.%s.10 dev c%s-eth%s" %(str(user_host_id), str(level_3_host_id), str(self.level_2_host_number+user_host_id)))
            self.level_3_host[level_3_host_id].cmdPrint("route add -net %s gw %s"%(str(self.redis_ip_subnet), str(switch_gw)))  

        '''user发出'''
        for user_host_id in range(self.user_host_number):
            for level_1_host_id in range(self.level_1_host_number):
                self.user_host[user_host_id].cmdPrint("route add -host 10.0.%s.1 dev u%s-eth%s" %(str(level_1_host_id), str(user_host_id), str(0)))
            for level_2_host_id in range(self.level_2_host_number):
                self.user_host[user_host_id].cmdPrint("route add -host 10.0.%s.3 dev u%s-eth%s" %(str(level_2_host_id), str(user_host_id), str(0)))
            for level_3_host_id in range(self.level_3_host_number):
                self.user_host[user_host_id].cmdPrint("route add -host 10.0.%s.5 dev u%s-eth%s" %(str(level_3_host_id), str(user_host_id), str(0)))
            self.user_host[user_host_id].cmdPrint("route add -net %s gw %s"%(str(self.redis_ip_subnet), str(switch_gw)))  


        print('*** Starting switches\n')
        '''需要加attach操作，来对switch绑定所有的eth。switch的eth下标从1开始'''

        for switch_id in range(self.level_1_host_number):
            for eth_id in range(1, self.level_2_host_number+2): # 和所有level_2_host相连，并连向指定level_1的host和外网
                self.switch[switch_id].attach('sw%s-eth%s'%(str(switch_id), str(eth_id)))
        for switch_id in range(self.level_1_host_number, self.level_1_host_number+self.level_2_host_number):
            for eth_id in range(1, self.level_3_host_number+2): # 和所有level_3_host相连，并连向指定level_2的host和外网
                self.switch[switch_id].attach('sw%s-eth%s'%(str(switch_id), str(eth_id)))
        for switch_id in range(self.level_1_host_number+self.level_2_host_number, self.level_1_host_number+self.level_2_host_number+self.user_host_number):
            for eth_id in range(1, self.level_1_host_number+self.level_2_host_number+self.level_3_host_number+2): # 和所有level的host相连，并连向指定user的host和外网
                self.switch[switch_id].attach('sw%s-eth%s'%(str(switch_id), str(eth_id)))
        for eth_id in range(1, self.level_1_host_number+self.level_2_host_number+self.level_3_host_number+self.user_host_number+1): ## 所有点和外网相连的switch
            self.switch[self.switch_number-1].attach('sw%s-eth%s'%(str(self.switch_number-1), str(eth_id)))

        print( '*** Starting network\n')
        '''创建网络'''
        self.net.build()

        '''删除默认路由，防止错误路由'''
        for level_1_host_id in range(self.level_1_host_number):
            self.level_1_host[level_1_host_id].cmdPrint("route del -net 10.0.0.0 netmask 255.0.0.0") 
        for level_2_host_id in range(self.level_2_host_number):
            self.level_2_host[level_2_host_id].cmdPrint("route del -net 10.0.0.0 netmask 255.0.0.0")
        for level_3_host_id in range(self.level_3_host_number):
            self.level_3_host[level_3_host_id].cmdPrint("route del -net 10.0.0.0 netmask 255.0.0.0")
        for user_host_id in range(self.user_host_number):
            self.user_host[user_host_id].cmdPrint("route del -net 10.0.0.0 netmask 255.0.0.0")

        '''等待30秒，保证网络构建完成'''
        time.sleep(30) 

    def run(self):
        '''构建网络拓扑'''
        self.myNetwork()

        setLogLevel( 'info' )

        # CLI(self.net)


# if __name__ == '__main__':
#     b = Build_network()
#     b.run()
#     CLI(b.net)
