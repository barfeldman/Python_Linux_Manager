**Service Management Script**

This Python script provides a command-line interface (CLI) for managing network interfaces and routes on Linux systems. It utilizes the netifaces and subprocess modules to interact with the system's network configuration.

**Features**
•	Change network adapter settings
•	Add routes to multicast addresses
•	Change hostname
•	Update service versions
•	Check connection to an installation machine

**Usage**
1.	Clone the repository:
git clone https://github.com/bfeldman/Python_Linux_Manager.git 
2.	Install the required Python packages:
pip install -r requirements.txt 
3.	Run the script:
python3 service.py 
4.	Follow the on-screen prompts to perform the desired actions.
   
**Example**
Change the network adapter settings:
Choose an action: 
1. Change network adapter 
2. Add route to multicast address 
3. Change hostname 
4. Update version of 'ela' service 
5. Check connection to Installation machine 
Enter '0' to quit Enter your choice [0]: 1 
Select a network interface: 
1. eth0 
2. wlan0 
Enter the number of the network interface you want to select: 1 
Current IP Address: 192.168.1.10 
Current Subnet Mask: 255.255.255.0 
Enter the new IP address: 192.168.1.20 
Enter the new subnet mask: 255.255.255.0 
**IP address and subnet mask updated successfully.**

**Notes**
•	This script requires sudo/root privileges to modify network settings.
•	Use with caution, as incorrect settings could disrupt network connectivity.

