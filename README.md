# Objective
This project aims to set up a small virtual enterprise network with Mininet. There will be a campus network and a home network connected to a computer cluster network. The network will have routing policies for various end devices with given constraints in different networks. The devices' access to the servers from the campus and home networks will follow the shortest best-performance link with the shortest path available. In addition, a firewall will be implemented to completely isolate Devices 1 and 2 (d1,d2) from the network to simulate the devices being compromised by a bad actor. This is the final assignment for CSE 150 - 01 Introduction to Computer Networks, 2021 Spring Quarter, taught by Christina Leigh Parsa. See FinalProject.pdf for more details.

Files submitted
-----------------
<p>final_dhcp.py: Topology code with dhcp for task 1<br>
final_skele.py: Topology code for task 2 and task 3<br>
task2_finalcontroller_skel.py: Controller code for task 2<br>
task3_finalcontroller_skel.py: Controller code for task 3</p>

Task 1: Topology
------------------
To start topology place it in ~ and run the command:
sudo python ~/final_dhcp.py

To clear controllers:
sudo mn -c 

DHCP server1 for h1-h4:<br>
sudo ~/pox/pox.py proto.dhcpd --network=10.1.1.0/24 --ip=10.1.1.1 --first=1 --last=None

DHCP server2 for d1 and d2 (Have to stop DHCP server1 first):<br>
sudo ~/pox/pox.py proto.dhcpd --network=10.2.2.0/24 --ip=10.2.2.1 --first=1 --last=None

<p>Testing:<br>
1.Start DHCP server1 in one terminal and then final_dhcp in another terminal<br>
2.Use the command dump to see all the switches and hosts with their IP addresses. You should see that the DHCP server assigned IP addresses to the campus network hosts:</p>

```
<Host h1: h1-eth0:10.1.1.10 pid=18860\>
<Host h2: h2-eth0:10.1.1.11 pid=18862\> 
<Host h3: h3-eth0:10.1.1.12 pid=18864\> 
<Host h4: h4-eth0:10.1.1.13 pid=18866\>
```

Use the command links to see the connected links.

3.In final_dhcp.py, comment the h1,h2,h3,h4 assignment part in the configure() function and then uncomment the d1 and d2 assignment part and save.<br>
4.Stop dhcp server1 and in the same terminal run dhcp server 2 and run final_dhcp.py again.<br>
5.Repeat step 2. You should see that the DHCP server assigned d1 and d2 with these IP addresses: 
```
<Host d1: d1-eth0:10.2.2.2 pid=21207> 
<Host d2: d2-eth0:10.2.2.3 pid=21209> 
```
Task 2: Routing
-----------------
As per instructions, the controller file for task2 and task 3 needs to be placed in \~/pox/pox/misc and mininet file (final_skel.py) needs to be placed in your home directory (~).

To start controller:<br>
sudo ~/pox/pox.py misc.task2_finalcontroller_skel

To start topology:<br>
sudo python ~/final_skel.py

Testing:<br>
1.Start the controller in one terminal and then final_skel in another terminal<br>
2.Use the command pingall. You should see:
```
CCServer1 -> CCServer2 d1 d2 h1 h2 h3 h4 
CCServer2 -> CCServer1 X X X X X X 
d1 -> CCServer1 X d2 h1 h2 h3 h4 
d2 -> CCServer1 X d1 h1 h2 h3 h4 
h1 -> CCServer1 X d1 d2 h2 h3 h4 
h2 -> CCServer1 X d1 d2 h1 h3 h4 
h3 -> CCServer1 X d1 d2 h1 h2 h4 
h4 -> CCServer1 X d1 d2 h1 h2 h3 
```
Since task 2 is about routing the shortest path between certain networks with the best performance link, I've hardcoded the paths in that way. I've used the source and destination IP addresses to figure out where the packet is going and switch_id to determine where a packet was received from. To send out the packet, the send function sends the packet to a specific port.
```
Pseudocode:
check if IP packet
   	check switch ID for packet's current location
    	check destination ip and send out of port
```
Campus network (h1, h2, h3, h4) -> Home network (d1, d2):<br>
switch1 -> switch3<br>

In task 1, we only care about the campus network reaching the home network so h1-h4 should path to reach d1 and d2 and the only path is switch1 to switch3. In the code, the link ports between s1 and s3 are 16 and 34. In lines 63 and 78, we see that based on the switch_id and IP destination, we send the packet through either 16 or 34. So by pinging, we can see that the campus network hosts successfully reached the home network hosts and vice versa.<br>

Campus network (h1, h2, h3, h4) -> Computing Cluster network (CCServer1, CCServer2):<br>
switch1 -> switch2 -> switch4<br>

The reason why this route was chosen to reach CCServer1 instead of CCServer2 was because the link between switch 4 and CCServer1 has a greater bandwidth (best performance) than the link between switch5 and CCServer2. When pinging the campus network to the computing cluster network, we don't care about CCServer2 because CCServer1 is the shortest path so h1-h4 should only reach CCServer1 and vice versa.<br>

Task 3: Firewall
------------------
To start controller:<br>
sudo ~/pox/pox.py misc.task3_finalcontroller_skel

To start topology:<br>
sudo python ~/final_skel.py

Testing:<br>
1.Start the controller in one terminal and then final_skel in another terminal<br>
2.Use the command pingall. You should see:
```
CCServer1 -> CCServer2 X X h1 h2 h3 h4
CCServer2 -> CCServer1 X X X X X X 
d1 -> X X X X X X X 
d2 -> X X X X X X X 
h1 -> CCServer1 X X X h2 h3 h4 
h2 -> CCServer1 X X X h1 h3 h4 
h3 -> CCServer1 X X X h1 h2 h4 
h4 -> CCServer1 X X X h1 h2 h3 
```
As we can see, d1 or d2 cannot send or receive any ICMP packets while the other hosts can communicate with each other. This is done by adding a rule to drop the packet if the source or destination IP address is from the home network.