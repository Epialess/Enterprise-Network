#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import RemoteController

class final_dhcp(Topo):

  def build(self):

    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    s4 = self.addSwitch('s4')
    s5 = self.addSwitch('s5')

    # Campus Network
    h1 = self.addHost('h1', ip='no ip defined/24')
    h2 = self.addHost('h2', ip='no ip defined/24')
    h3 = self.addHost('h3', ip='no ip defined/24')
    h4 = self.addHost('h4', ip='no ip defined/24')

    # Home Network
    d1 = self.addHost('d1', ip='no ip defined/24')
    d2 = self.addHost('d2', ip='no ip defined/24')

    # Computing Cluster Network
    CCServer1 = self.addHost('CCServer1', ip='10.3.3.1/29')
    CCServer2 = self.addHost('CCServer2', ip='10.3.3.2/29')

    # connect campus network with switch
    self.addLink(h1,s1,bw=3)
    self.addLink(h2,s1,bw=3)
    self.addLink(h3,s1,bw=3)
    self.addLink(h4,s1,bw=3)

    # links between switches
    self.addLink(s1,s2,bw=3)
    self.addLink(s1,s3,bw=3)
    self.addLink(s1,s5,bw=3)
    self.addLink(s2,s4,bw=3)
    self.addLink(s3,s5,bw=3)
    self.addLink(s4,s5,bw=3)

    # connect home network with switch
    self.addLink(d1,s3,bw=3)
    self.addLink(d2,s3,bw=3)

    # connect computing cluster network with switch
    self.addLink(CCServer1,s4,bw=10)
    self.addLink(CCServer2,s5,bw=3)


def configure():

  topo = final_dhcp()

  net = Mininet(topo=topo, link = TCLink, controller=RemoteController)

  net.start()

  h1, h2, h3, h4, d1, d2, CCServer1, CCServer2 = net.get('h1', 'h2', 'h3', 
                            'h4', 'd1', 'd2', 'CCServer1', 'CCServer2')
  
  print("*** enable dhcpclient, and assign ip address to campus network ***")
  h1.cmd('sudo dhclient h1-eth0')
  h2.cmd('sudo dhclient h2-eth0')
  h3.cmd('sudo dhclient h3-eth0')
  h4.cmd('sudo dhclient h4-eth0')

  intf_h1 = net.get('h1').defaultIntf()
  intf_h2 = net.get('h2').defaultIntf()
  intf_h3 = net.get('h3').defaultIntf()
  intf_h4 = net.get('h4').defaultIntf()

  intf_h1.updateIP()
  intf_h2.updateIP()
  intf_h3.updateIP()
  intf_h4.updateIP()

  # print("*** enable dhcpclient, and assign ip address to home network***")
  # d1.cmd('sudo dhclient d1-eth0')
  # d2.cmd('sudo dhclient d2-eth0')

  # intf_d1 = net.get('d1').defaultIntf()
  # intf_d2 = net.get('d2').defaultIntf()

  # intf_d1.updateIP()
  # intf_d2.updateIP()


  
  CLI(net)
  net.stop()


if __name__ == '__main__':
  configure()

