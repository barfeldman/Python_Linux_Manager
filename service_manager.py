import click
import netifaces
import subprocess

@click.command()
def main():
    while True:
        click.echo("Choose an action:")
        click.echo("1. Change network adapter")
        click.echo("2. Add route to multicast address")
        click.echo("3. Change hostname")
        click.echo("4. Update version of 'ela' service")
        click.echo("5. Check connection to Installation machine")
        click.echo("Enter '0' to quit")

        choice = click.prompt("Enter your choice", type=int, default=0)

        if choice == 1:
            change_network_adapter()
        elif choice == 2:
            add_route_to_multicast_address()
        elif choice == 3:
            change_hostname()
        elif choice == 4:
            update_ela_service()
        elif choice == 5:
            check_connection()
        elif choice == 0:
            break
        else:
            click.echo("Invalid choice. Please try again.")

        if not click.confirm("Do you want to proceed with more actions?", default=True):
            break



def get_network_interface_address(interface_name):
    addresses = netifaces.ifaddresses(interface_name)
    ipv4_info = addresses.get(netifaces.AF_INET)
    if ipv4_info:
        ip_address = ipv4_info[0]['addr']
        subnet_mask = ipv4_info[0]['netmask']
        return ip_address, subnet_mask
    return None, None

def set_network_interface_address(interface_name, ip_address, subnet_mask):
    subprocess.run(["sudo", "ip", "addr", "flush", "dev", interface_name])
    subprocess.run(["sudo", "ip", "addr", "add", f"{ip_address}/{subnet_mask}", "dev", interface_name])



def change_network_adapter():
    interfaces = netifaces.interfaces()
    filtered_interfaces = [interface for interface in interfaces if any(substring in interface.lower() for substring in ["ens", "eth", "ext", "int", "eno", "dummy"])] #dummy just for tests

    if not filtered_interfaces:
        print("No network interfaces found.")
    else:
        print("Select a network interface:")
        for idx, interface in enumerate(filtered_interfaces, start=1):
            print(f"{idx}. {interface}")

        while True:
            choice = input("Enter the number of the network interface you want to select: ")
            try:
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(filtered_interfaces):
                    selected_interface = filtered_interfaces[choice_idx - 1]
                    ip_address, subnet_mask = get_network_interface_address(selected_interface)
                    print(f"Current IP Address: {ip_address}")
                    print(f"Current Subnet Mask: {subnet_mask}")

                    new_ip_address = input("Enter the new IP address: ")
                    new_subnet_mask = input("Enter the new subnet mask: ")

                    set_network_interface_address(selected_interface, new_ip_address, new_subnet_mask)
                    print("IP address and subnet mask updated successfully.")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def add_route_to_multicast_address():
    interfaces = netifaces.interfaces()
    filtered_interfaces = [interface for interface in interfaces if any(substring in interface.lower() for substring in ["ens", "eth", "ext", "int", "dummy"])]

    if not filtered_interfaces:
        print("No network interfaces containing 'ens', 'eth', 'ext', 'int', or 'dummy' found.")
    else:
        print("Select a network interface:")
        for idx, interface in enumerate(filtered_interfaces, start=1):
            print(f"{idx}. {interface}")

        while True:
            choice = input("Enter the number of the network interface you want to select: ")
            try:
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(filtered_interfaces):
                    selected_interface = filtered_interfaces[choice_idx - 1]

                    # Check if the interface is up and bring it up if it's not
                    if not is_interface_up(selected_interface):
                        bring_interface_up(selected_interface)
                    
                    multicast_address = input("Enter the multicast address (e.g., 224.0.0.1): ")
                    metric = input("Enter the metric (default is 100, if its ok press enter): ") or "100"
                    subnet_mask = input("Enter the subnet mask (default is 8, if its ok press enter): ") or "8"

                    try:
                        subprocess.run(["sudo", "ip", "route", "add", f"{multicast_address}/{subnet_mask}", "dev", selected_interface, "metric", metric])
                        print("Route to multicast address added successfully.")
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to add route: {e}")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

def is_interface_up(interface_name):
    # Check if the interface is up by checking its flags
    flags = netifaces.ifaddresses(interface_name)
    return netifaces.AF_INET in flags

def bring_interface_up(interface_name):
    subprocess.run(["sudo", "ip", "link", "set", "dev", interface_name, "up"])
    print(f"Interface {interface_name} is now up.")

def change_hostname():
    click.echo(click.style("Changing hostname...", fg='green'))

def update_ela_service():
    click.echo(click.style("Updating ela service...", fg='green'))

def check_connection():
    click.echo(click.style("Checking connection to Installation machine...", fg='green'))

if __name__ == "__main__":
    main()
