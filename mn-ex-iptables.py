#!/usr/bin/python

import time
import sys
import argparse
import math
import os

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.clean import cleanup


class NetTopo(Topo):
	def build(self, **_opts):
		s1 = self.addSwitch('s1')
		pc1 = self.addHost('pc1')
		pc2 = self.addHost('pc2')

		s2 = self.addSwitch('s2')
		srv1 = self.addHost('srv1')
		srv2 = self.addHost('srv2')

		r1 = self.addHost('r1')
		r2 = self.addHost('r2')

		self.addLink(s1, r1, intfName1='s1-eth0', intfName2='r1-eth0')
		self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth1')
		self.addLink(s2, r2, intfName1='s2-eth0', intfName2='r2-eth0')

		self.addLink(pc1, s1, intfName1='pc1-eth0', intfName2='s1-eth1')
		self.addLink(pc2, s1, intfName1='pc2-eth0', intfName2='s1-eth2')

		self.addLink(srv1, s2, intfName1='srv1-eth0', intfName2='s2-eth1')
		self.addLink(srv2, s2, intfName1='srv2-eth0', intfName2='s2-eth2')



def create_ip_net(net):
	print "create_ip_net"

	net['r1'].cmdPrint("ifconfig r1-eth0 192.168.0.1/24")
	net['pc1'].cmdPrint("ifconfig pc1-eth0 192.168.0.10/24")
	net['pc2'].cmdPrint("ifconfig pc2-eth0 192.168.0.20/24")


	net['r2'].cmdPrint("ifconfig r2-eth0 200.131.132.1/24")
	net['srv1'].cmdPrint("ifconfig srv1-eth0 200.131.132.10/24")
	net['srv2'].cmdPrint("ifconfig srv2-eth0 200.131.132.20/24")

	net['r1'].cmdPrint("ifconfig r1-eth1 143.107.231.1/24")
	net['r2'].cmdPrint("ifconfig r2-eth1 143.107.231.2/24")

def config_static_route(net):
	print "setting static routes on client and server nodes"
        net['r1'].cmdPrint('route add -net 200.131.132.0/24 gw 143.107.231.2')
        #net['r2'].cmdPrint('route add -net 143.107.231.0/24 gw 143.107.231.1')

	net['pc1'].cmdPrint('route add default gw 192.168.0.1')
	net['pc2'].cmdPrint('route add default gw 192.168.0.1')

	net['srv1'].cmdPrint('route add default gw 200.131.132.1')
	net['srv2'].cmdPrint('route add default gw 200.131.132.1')

	net['r1'].cmdPrint('sysctl -w net.ipv4.ip_forward=1')
	net['r2'].cmdPrint('sysctl -w net.ipv4.ip_forward=1')


def net_test(net):
	print "Network connectivity"
	net['c'].cmdPrint('ping -c 20 193.1.2.2')
	net['c'].cmdPrint('traceroute 193.1.2.2')
	net['s'].cmdPrint('iperf3 -s &')
	net['c'].cmdPrint('sleep 3')
	net['c'].cmdPrint('iperf3 -c 193.1.2.2 -R -t 10 -P 2')

def iptables(net):
	net['r1'].cmdPrint('sh r1_rules.sh')
def run():
	topo = NetTopo()
	net = Mininet(topo=topo, link=TCLink, controller=Controller)
	net.start()
	print "Host connections"
	dumpNodeConnections(net.hosts)

	create_ip_net(net)
	config_static_route(net)
	iptables(net)

	#net_test(net)

	CLI(net)
	net.stop()
	cleanup()


if __name__ == '__main__':
	setLogLevel( 'info' )
	run()
