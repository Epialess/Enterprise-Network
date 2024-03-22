# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

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

  def send (self, packet, packet_in, port_in):
    # Send the packet to specific ports
    msg = of.ofp_packet_out()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    
    msg.actions.append(of.ofp_action_output(port = port_in))
    msg.data = packet_in
    msg.in_port = port_in
    self.connection.send(msg)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    def drop ():
      # Drop the packet and create rule
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    def flood ():
      # Flood the packet to all ports
      msg = of.ofp_packet_out()
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      msg.data = packet_in
      msg.in_port = in_port
      self.connection.send(msg)


    ip = packet.find('ipv4')
    # Check if is IP type 
    if ip is not None:
      ip_packet = packet.payload

      # Handles ICMP packet
      if ip_packet.protocol == ip_packet.ICMP_PROTOCOL:

        # If source ip is a client and dest ip is a server
        # client -> server: drop
        if ip_packet.srcip in homeAddresses and ip_packet.dstip in campusAddresses:
          send(packet, packet_in, 4) # send to s1
          if switch_id == 6: # port that s1 receives on from s3
            if ip_packet.dstip == "10.1.1.10":
              send(packet, packet_in, 1)
            if ip_packet.dstip == "10.1.1.11":
              send(packet, packet_in, 2)
            if ip_packet.dstip == "10.1.1.12":
              send(packet, packet_in, 3)
            if ip_packet.dstip == "10.1.1.13":
              send(packet, packet_in, 4)
    # Else, accept it
    else:
      flood()

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
