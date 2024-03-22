#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):

    # Switches
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    s4 = self.addSwitch('s4')
    s5 = self.addSwitch('s5')

    # Campus Network
    h1 = self.addHost('h1', ip='10.1.1.10/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2', ip='10.1.1.11/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3', ip='10.1.1.12/24', defaultRoute="h3-eth0")
    h4 = self.addHost('h4', ip='10.1.1.13/24', defaultRoute="h4-eth0")

    # Home Network
    d1 = self.addHost('d1', ip='10.2.2.2/24', defaultRoute="d1-eth0")
    d2 = self.addHost('d2', ip='10.2.2.3/24', defaultRoute="d2-eth0")

    # Computing Cluster Network
    CCServer1 = self.addHost('CCServer1', ip='10.3.3.1/29', defaultRoute="CCServer1-eth0")
    CCServer2 = self.addHost('CCServer2', ip='10.3.3.2/29', defaultRoute="CCServer2-eth0")
    
    # Assign links with bandwidth and ports
    # h# -> s1
    self.addLink(h1,s1, bw=3, port1=0, port2=11)
    self.addLink(h2,s1, bw=3, port1=0, port2=12)
    self.addLink(h3,s1, bw=3, port1=0, port2=13)
    self.addLink(h4,s1, bw=3, port1=0, port2=14)

    # links between switches
    self.addLink(s1,s2, bw=3, port1=15, port2=21)
    self.addLink(s1,s3, bw=3, port1=16, port2=34)
    # self.addLink(s1,s5, bw=3, port1=17, port2=3)
    self.addLink(s2,s4, bw=3, port1=22, port2=42)
    self.addLink(s3,s5, bw=3, port1=33, port2=54)
    # self.addLink(s4,s5, bw=3, port1=43, port2=52)

    # d# -> s3
    self.addLink(d1,s3, bw=3, port1=0, port2=31)
    self.addLink(d2,s3, bw=3, port1=0, port2=32)

    # ccs1 -> s4, ccs2 -> s5
    self.addLink(CCServer1,s4, bw=10, port1=0, port2=41)
    self.addLink(CCServer2,s5, bw=3, port1=0, port2=51)

    
    

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, link = TCLink, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
