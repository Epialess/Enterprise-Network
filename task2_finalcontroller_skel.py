# Final Skeleton for task 2

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

homeAddresses = ["10.2.2.2", "10.2.2.3"]
campusAddresses = ["10.1.1.10","10.1.1.11","10.1.1.12","10.1.1.13"]
ccsAddresses = ["10.3.3.1", "10.3.3.2"]

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    def drop ():
      # Drop the packet and create rule
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    def send (port_in):
      # Send the packet to specific ports
      msg = of.ofp_packet_out()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      
      msg.actions.append(of.ofp_action_output(port = port_in))
      msg.data = packet_in
      self.connection.send(msg)

    ip = packet.find('ipv4')
    # Check if is IP type 
    if ip is not None:
      ip_packet = packet.payload

      # Handles ICMP/TCP packet
      if ip_packet.protocol == ip_packet.ICMP_PROTOCOL or ip_packet.protocol == ip_packet.TCP_PROTOCOL:
        # Chained if else to determine destination port
        if switch_id == 1:
          if ip_packet.dstip == "10.1.1.10":
            send(11)
          elif ip_packet.dstip == "10.1.1.11":
            send(12)
          elif ip_packet.dstip == "10.1.1.12":
            send(13)
          elif ip_packet.dstip == "10.1.1.13":
            send(14)
          elif ip_packet.dstip == "10.3.3.1":
            send(15)
          elif ip_packet.dstip in homeAddresses or ip_packet.dstip == "10.3.3.2":
            send(16)
        if switch_id == 2:     
          if ip_packet.dstip in campusAddresses or ip_packet.dstip in homeAddresses or ip_packet.dstip == "10.3.3.2":
            send(21)
          elif ip_packet.dstip == "10.3.3.1":
            send(22)
        if switch_id == 3:
          if ip_packet.dstip == "10.2.2.2":
            send(31)
          elif ip_packet.dstip == "10.2.2.3":
            send(32)
          elif ip_packet.dstip == "10.3.3.2":
            send(33)              
          elif ip_packet.dstip == "10.3.3.1" or ip_packet.dstip in campusAddresses:
            send(34)  
        if switch_id == 4:
          if ip_packet.dstip in campusAddresses or ip_packet.dstip in homeAddresses or ip_packet.dstip == "10.3.3.2":
            send(42)
          elif ip_packet.dstip == "10.3.3.1":
            send(41)
        if switch_id == 5:
          if ip_packet.dstip == "10.3.3.1":
            send(54)
          elif ip_packet.dstip == "10.3.3.2":
            send(51)
          
    else: # flood all ports
      send(of.OFPP_FLOOD)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
