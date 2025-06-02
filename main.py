from colorama import Fore, Style
import SmartDevice
import time
from abc import ABC, abstractmethod
import Network
import User

"""Each device will be attached to 1 network
devices can be under a hub
each smarthome is connected to 1 network
a user is not set by a network but can only be in 1 at a time
users can see their other devices in other networks not currently connected to
users are not directly connected to smartdevices, the creation of a smarthome is required first
there can be multiple smarthomes in a network
users connected to a network can see all the smarthomes in that network"""
#figure out a way to manage time with a text based gui




class GUI():
    def __init__(self):
        self.users = []
        self.networks = []
        self.logged_in_user = None
        self.connected_network = None
        self.schedualed_operations = []

    def add_user(self, user):
        self.users.append(user)

    def add_network(self, network):
        self.networks.append(network)

    def set_logged_in_user(self, user):
        self.logged_in_user = user

    def set_connected_network(self, network):
        self.connected_network = network

    def logged_out(self):
        print(Fore.CYAN + "Welcome to the Smart Home System!" + Style.RESET_ALL)
        print("1. Create a new user")
        print("2. log in")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            user = next((user for user in self.users if user.username == username), None)
            if user:
                print(Fore.RED + f"Username {username} already exists" + Style.RESET_ALL)
                return False
            try:
                self.logged_in_user = User.User(username)
                self.logged_in_user.connect_to_network(self.connected_network)
                self.users.append(self.logged_in_user)
                print(Fore.GREEN + f"User {username} created successfully!" + Style.RESET_ALL)
                return False
            except ValueError as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
                return False
        elif choice == "2":
            username = input("Enter your username: ")
            user = next((user for user in self.users if user.username == username), None)
            if user:
                print(Fore.GREEN + f"Welcome back, {username}!" + Style.RESET_ALL)
                return False
            else:
                print(Fore.RED + "User not found. Please create a new user." + Style.RESET_ALL)
                return False
        elif choice == "3":
            print(Fore.RED + "Exiting the system." + Style.RESET_ALL)
            return True
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)
            return False

    def logged_in(self):
        time.sleep(1)
        print(Fore.CYAN + "Welcome to the Smart Home System!" + Style.RESET_ALL)
        if self.connected_network is not None:
            print(Fore.GREEN + f"Connected to network: {self.connected_network.ip_address}" + Style.RESET_ALL)
            print("1. Create a new smart home")
            print("2. Select a smart home")
            print("3. List smart homes")
            print("4. Create a new device")
            print("5. List devices in network")
            print("6. Select a device")
            print("7. Select Network")
        else:
            print("1. Connect to Network")
        print("0. Log out")
        choice = input("Enter your choice: ")
        #Create a new smart home
        if choice == "1" and self.connected_network is not None:
            name = input("Enter a name for your smart home: ")
            smart_home = User.SmartHome(self.logged_in_user.network, name)
            self.connected_network.add_smart_home(smart_home)
            print(Fore.GREEN + f"Smart home {name} created successfully!" + Style.RESET_ALL)
            return False
        #Select a smart home
        elif choice == "2" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
                return False
            print("List of Smart Homes:")
            for i in self.connected_network.list_smart_homes():
                print(i)
            smart_home_name = input("Enter the name of the smart home: ")
            smart_home = next((home for home in self.connected_network.smart_homes if home.name == smart_home_name), None)
            if smart_home:
                print(Fore.GREEN + f"Selected smart home: {smart_home}" + Style.RESET_ALL)
                self.home_details(smart_home)
                return False
            else:
                print(Fore.RED + "Smart home not found." + Style.RESET_ALL)
        #List smart homes
        elif choice == "3" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found." + Style.RESET_ALL)
                return False
            print("List of Smart Homes:")
            for i in self.connected_network.list_smart_homes():
                print(i)
        #Create a new device
        elif choice == "4" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
                return False
            name = input("Enter a name for your device: ")
            print("List of Device Types:")
            print("1. Light")
            print("2. Thermostat")
            print("3. Camera")
            print("4. Lock")
            print("5. Speaker")
            print("6. Doorbell")
            print("7. Door")
            print("8. Appliance")
            print("9. None")
            device_type_choice = input("Enter the number of the device type: ")
            device_types = {
                "1": "Light",
                "2": "Thermostat",
                "3": "Camera",
                "4": "Lock",
                "5": "Speaker",
                "6": "Doorbell",
                "7": "Door",
                "8": "Appliance",
                "9": "None"
            }
            device_type = device_types.get(device_type_choice)
            if device_type == "None":
                device_type = input("Enter the type of device: ")
            smart_home_name = input("Enter the name of the smart home to add the device to: ")
            smart_home = next((home for home in self.connected_network.smart_homes if home.name == smart_home_name), None)
            if smart_home:
                if device_type == "Light":
                    device = SmartDevice.SmartLight(name)
                elif device_type == "Thermostat":
                    device = SmartDevice.SmartThermostat(name)
                elif device_type == "Camera":
                    device = SmartDevice.SmartCamera(name)
                elif device_type == "Lock":
                    device = SmartDevice.SmartLock(name)
                elif device_type == "Speaker":
                    device = SmartDevice.SmartSpeaker(name)
                elif device_type == "Doorbell":
                    device = SmartDevice.SmartDoorbell(name)
                elif device_type == "Door":
                    device = SmartDevice.SmartDoor(name)
                elif device_type == "Appliance":
                    device = SmartDevice.SmartAppliance(name)
                else:
                    device = SmartDevice.SmartDevice(name, device_type)
                smart_home.add_smart_device(device)
                print(Fore.GREEN + f"Device {name} created successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Smart home not found." + Style.RESET_ALL)
        #List devices in network
        elif choice == "5" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
                return False
            print("Devices in Network:")
            for home in self.connected_network.smart_homes:
                print(f"Smart Home: {home.name}")
                for device in home.smart_devices:
                    print(f"  Device: {device.name} ({device.device_type})")
        #Select a device
        elif choice == "6" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
                return False
            print("\nAvailable Smart Homes:")
            for idx, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  [{idx}] {home.name}")
            try:
                home_idx = int(input("Select a smart home by number: ")) - 1
                smart_home = self.connected_network.smart_homes[home_idx]
            except (ValueError, IndexError):
                print(Fore.RED + "Invalid selection. Please enter a valid number." + Style.RESET_ALL)
                return False
            if not smart_home.smart_devices:
                print(Fore.RED + f"No devices found in {smart_home.name}." + Style.RESET_ALL)
                return False
            print(f"\nDevices in {smart_home.name}:")
            for idx, device in enumerate(smart_home.smart_devices, 1):
                print(f"  [{idx}] {device.name} ({device.device_type})")
            try:
                device_idx = int(input("Select a device by number: ")) - 1
                device = smart_home.smart_devices[device_idx]
            except (ValueError, IndexError):
                print(Fore.RED + "Invalid selection. Please enter a valid number." + Style.RESET_ALL)
                return False
            print(Fore.GREEN + f"Selected device: {device}" + Style.RESET_ALL)
            self.device_details(device, smart_home)
            return False
        #Select Network
        elif choice == "7" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
                return False
            self.network_details()
        #Log out
        elif choice == "0":
            print(Fore.RED + f"Logging out {self.logged_in_user.username}..." + Style.RESET_ALL)
            self.logged_in_user.disconnect_from_network()
            self.logged_in_user = None
            return False
        #Connect to Network
        elif choice == "1" and self.connected_network is None:
            print("Available Networks:")
            for network in self.networks:
                print(network.ip_address)
            ip_address = input("Enter the IP address of the network to connect to: ")
            network = next((net for net in self.networks if net.ip_address == ip_address), None)
            if network:
                try:
                    self.logged_in_user.connect_to_network(network)
                    self.connected_network = network
                    print(Fore.GREEN + f"Connected to network: {network.ip_address}" + Style.RESET_ALL)
                except ValueError as e:
                    print(Fore.RED + str(e) + Style.RESET_ALL)
            else:
                print(Fore.RED + "Network not found." + Style.RESET_ALL)
        return False

    def device_details(self, device, home):
        print("1. Turn on/off device")
        print("2. Get device status")
        print("3. Delete device")
        choice = input("Enter your choice: ")
        if choice == "1":
            device.toggle()
        elif choice == "2":
            print(Fore.GREEN + f"{repr(device)}" + Style.RESET_ALL)
        elif choice == "3":
            try:
                home.remove_smart_device(device)
            except:
                print(Fore.RED + "Cannot delete device: smart home reference not found." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)

    def home_details(self, home):
        print("1. List devices")
        print("2. Secure home")
        print("3. Delete home")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(Fore.GREEN + f"Devices in {home.name}:" + Style.RESET_ALL)
            for device in home.smart_devices:
                print(device)
        elif choice == "2":
            home.secure_home()
        elif choice == "3":
            try:
                self.connected_network.remove_smart_home(home)
            except:
                print(Fore.RED + "Cannot delete smart home: network reference not found." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)

    def network_details(self):
        print("1. List smart homes")
        print("2. Add smart home")
        print("3. Remove smart home")
        print("4. List devices in network")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(Fore.GREEN + f"Smart homes in network {self.connected_network.ip_address}:" + Style.RESET_ALL)
            for home in self.connected_network.smart_homes:
                print(home)
        elif choice == "2":
            name = input("Enter a name for the smart home: ")
            smart_home = User.SmartHome(self.connected_network, name)
            self.connected_network.add_smart_home(smart_home)
            print(Fore.GREEN + f"Smart home {name} added successfully!" + Style.RESET_ALL)
        elif choice == "3":
            name = input("Enter the name of the smart home to remove: ")
            smart_home = next((home for home in self.connected_network.smart_homes if home.name == name), None)
            if smart_home:
                self.connected_network.remove_smart_home(smart_home)
                print(Fore.GREEN + f"Smart home {name} removed successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Smart home not found." + Style.RESET_ALL)
        elif choice == "4":
            self.connected_network.list_devices_in_network()
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)


    def loop(self):
        while True:
            if self.logged_in_user is None:
                x = self.logged_out()
            else:
                x = self.logged_in()
            if x:
                break
            time.sleep(1)

    def opperation_check(self):
        if self.schedualed_operations:
            for operation in self.schedualed_operations:
                if operation['time'] <= time.time():
                    try:
                        operation['function'](*operation['args'], **operation['kwargs'])
                        self.schedualed_operations.remove(operation)
                    except Exception as e:
                        print(Fore.RED + f"Error during scheduled operation: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    gui = GUI()
    gui.connected_network = Network.Network("19")
    gui.networks.append(gui.connected_network)
    gui.loop()

