============================
Name: Andy Choi
Email: Achoi15@ucsc.edu
Cruz ID: Achoi15
Student ID number: 1674488
============================
-----------------
Files submitted
-----------------
final_dhcp.py: Topology code with dhcp for task 1
final_skele.py: Topology code for task 2 and task 3
task2_finalcontroller_skel.py: Controller code for task 2
task3_finalcontroller_skel.py: Controller code for task 3

------------------
Task 1: Topology
------------------
To start topology place it in ~ and run the command:
sudo python ~/final_dhcp.py

To clear controllers:
sudo mn -c 

DHCP server1 for h1-h4:
sudo ~/pox/pox.py proto.dhcpd --network=10.1.1.0/24 --ip=10.1.1.1 --first=1 --last=None

DHCP server2 for d1 and d2 (Have to stop DHCP server1 first):
sudo ~/pox/pox.py proto.dhcpd --network=10.2.2.0/24 --ip=10.2.2.1 --first=1 --last=None

Testing:
1.Start dhcp server1 in one terminal and then final_dhcp in another terminal
2.Use the command dump to see all the switches and hosts with their IP addresses. You should see that the dhcp server assigned IP addresses to the campus network hosts:

<Host h1: h1-eth0:10.1.1.10 pid=18860> 
<Host h2: h2-eth0:10.1.1.11 pid=18862> 
<Host h3: h3-eth0:10.1.1.12 pid=18864> 
<Host h4: h4-eth0:10.1.1.13 pid=18866> 

Use the command links to see the connected links.

3.In final_dhcp.py, comment the h1,h2,h3,h4 assignment part in the configure() function and then uncomment the d1 and d2 assignment part and save.
4.Stop dhcp server1 and in the same terminal run dhcp server 2 and run final_dhcp.py again.
5.Repeat step 2. You should see that the dhcp server assigned d1 and d2 with these IP addresses: 

<Host d1: d1-eth0:10.2.2.2 pid=21207> 
<Host d2: d2-eth0:10.2.2.3 pid=21209> 


-----------------
Task 2: Routing
-----------------
As per instructions, the controller file for task2 and task 3 needs to be placed in ~/pox/pox/misc and mininet file (final_skel.py) needs to be placed in your home directory (~).

To start controller:
sudo ~/pox/pox.py misc.task2_finalcontroller_skel

To start topology:
sudo python ~/final_skel.py

Testing:
1.Start the controller in one terminal and then final_skel in another terminal
2.Use the command pingall. You should see:

CCServer1 -> CCServer2 d1 d2 h1 h2 h3 h4 
CCServer2 -> CCServer1 X X X X X X 
d1 -> CCServer1 X d2 h1 h2 h3 h4 
d2 -> CCServer1 X d1 h1 h2 h3 h4 
h1 -> CCServer1 X d1 d2 h2 h3 h4 
h2 -> CCServer1 X d1 d2 h1 h3 h4 
h3 -> CCServer1 X d1 d2 h1 h2 h4 
h4 -> CCServer1 X d1 d2 h1 h2 h3 

Since task 2 is about routing the shortest path between certain networks with the best performance link, I've hardcoded the paths in that way. I've use the source and destination IP addresses to figure out where the packet is going and switch_id to determine where a packet was recieved from. To send out the packet, the send function sends the packet to a specific port.

Pseudocode:
check if IP packet
   	check switch ID for packet's current location
    	check destination ip and send out of port

Campus network (h1, h2, h3, h4) -> Home network (d1, d2):
switch1 -> switch3

In task 1, we only care about the campus network reaching the home network so h1-h4 should path to reach d1 and d2 and the only path is switch1 to switch3. In the code, the link ports between s1 and s3 are 16 and 34. In lines 63 and 78, we see that based on the switch_id and IP destination, we send the packet through either 16 or 34. So by pinging, we can see that the campus network hosts successfully reached the home network hosts and vice versa.

Campus network (h1, h2, h3, h4) -> Computing Cluster network (CCServer1, CCServer2):
switch1 -> switch2 -> switch4

The reason why this route was chosen to reach CCServer1 instead of CCServer2 was because the link between switch 4 and CCServer1 has a greater bandwidth (best performance) than the link between switch5 and CCServer2. When pinging the campus network to computing cluster network, we don't really care about CCServer2 because CCServer1 is the shortest path so h1-h4 should only reach CCServer1 and vice versa.

------------------
Task 3: Firewall
------------------
To start controller:
sudo ~/pox/pox.py misc.task3_finalcontroller_skel

To start topology:
sudo python ~/final_skel.py

Testing:
1.Start the controller in one terminal and then final_skel in another terminal
2.Use the command pingall. You should see:

CCServer1 -> CCServer2 X X h1 h2 h3 h4 
CCServer2 -> CCServer1 X X X X X X 
d1 -> X X X X X X X 
d2 -> X X X X X X X 
h1 -> CCServer1 X X X h2 h3 h4 
h2 -> CCServer1 X X X h1 h3 h4 
h3 -> CCServer1 X X X h1 h2 h4 
h4 -> CCServer1 X X X h1 h2 h3 

As we can see, d1 or d2 cannot send or receive any ping packets while the other hosts are able to communicate with each other. This is done by adding a rule to drop the packet if the source or destination IP address is from the home network.