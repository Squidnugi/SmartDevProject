from colorama import Fore, Style
import SmartDevice
import time
from abc import ABC, abstractmethod
import Network

"""Each device will be attached to 1 network
devices can be under a hub
each smarthome is connected to 1 network
a user is not set by a network but can only be in 1 at a time
users can see their other devices in other networks not currently connected to
users are not directly connected to smartdevices, the creation of a smarthome is required first
there can be multiple smarthomes in a network
users connected to a network can see all the smarthomes in that network"""


#each home is connected to a IP address and when a user connects to that IP address, they can access the smart devices in that home
class User:
    def __init__(self, username):
        if username.lower() in ["example", "test", "admin"]:
            raise ValueError("Username exists in the system. Please choose a different username.")
        self.username = username
        self.smart_homes = []
        self.network = None

    def __str__(self):
        return f"User: {self.username}"
    def __repr__(self):
        return f"User(username={self.username}, smart_devices={self.smart_homes})"

    def add_smart_home(self, smart_home):
        self.smart_homes.append(smart_home)
        print(f"{smart_home.name} has been added to {self.username}'s smart homes.")

    def connect_smart_home(self, smart_home):
        if smart_home not in self.smart_homes:
            print(f"{smart_home.name} is not in {self.username}'s smart homes.")
            return
        self.smart_homes.append(smart_home)
        print(f"{self.username} is now connected to {smart_home.name}.")

    def remove_smart_home(self, smart_home):
        self.smart_homes.remove(smart_home)
        print(f"{smart_home.name} has been removed from {self.username}'s smart homes.")

    def list_smart_homes(self):
        return [smart_home.name for smart_home in self.smart_homes]

    def list_devices(self):
        devices = []
        for smart_home in self.smart_homes:
            devices.extend(smart_home.list_devices())
        return devices

    def disconnect_smart_home(self, smart_home):
        if smart_home not in self.smart_homes:
            print(f"{smart_home.name} is not in {self.username}'s smart homes.")
            return
        self.smart_homes.remove(smart_home)
        print(f"{self.username} has disconnected from {smart_home.name}.")

    def connect_to_network(self, network):
        if not isinstance(network, Network.Network):
            raise TypeError("Can only connect to a Network instance.")
        self.network = network
        print(f"{self.username} is now connected to {network.ip_address}.")

    def disconnect_from_network(self):
        if self.network is None:
            print(f"{self.username} is not connected to any network.")
            return
        self.network = None
        print(f"{self.username} has disconnected from the network.")


class SmartHome:
    def __init__(self, network, name):
        self.users = []
        self.smart_hubs = []
        self.smart_devices = []
        self.network = network
        self.name = name
    def __str__(self):
        return f"SmartHome: {self.name}, Network: {self.network.ip_address}"
    def __repr__(self):
        return f"SmartHome(name={self.name}, network={self.network.ip_address}, users={self.users}, smart_hubs={self.smart_hubs}, smart_devices={self.smart_devices})"


    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def list_users(self):
        return [user.username for user in self.users]

    def add_smart_hub(self, smart_hub):
        self.smart_hubs.append(smart_hub)
        print(f"{smart_hub.name} has been added to {self.name}.")

    def remove_smart_hub(self, smart_hub):
        self.smart_hubs.remove(smart_hub)
        print(f"{smart_hub.name} has been removed from {self.name}.")

    def list_smart_hubs(self):
        return [smart_hub.name for smart_hub in self.smart_hubs]

    def add_smart_device(self, smart_device):
        self.smart_devices.append(smart_device)
        print(f"{smart_device.name} has been added to {self.name}.")

    def remove_smart_device(self, smart_device):
        self.smart_devices.remove(smart_device)
        print(f"{smart_device.name} has been removed from {self.name}.")

    def list_smart_devices(self):
        return [smart_device.name for smart_device in self.smart_devices]


if __name__ == "__main__":
    # Create a network
    network = Network.Network("192.168.1.1")
    print(network)
    # Create a user
    user = User("JohnDoe")
    print(user)
    # Create a smart home
    smart_home = SmartHome(network, "John's Smart Home")
    print(smart_home)
    # Add the smart home to the user
    user.add_smart_home(smart_home)
    # Connect the user to the network
    user.connect_to_network(network)
    # Create a smart hub
    smart_hub = SmartDevice.SmartHub("Living Room Hub")
    print(smart_hub)
    # Add the smart hub to the smart home
    smart_home.add_smart_hub(smart_hub)
    # Create a smart device
    smart_device = SmartDevice.SmartLight("Living Room Light", 75)
    print(smart_device)
    # Add the smart device to the smart hub
    smart_hub.add_device(smart_device)
    # List all smart devices in the smart home
    print("Smart devices in the smart home:")
    print(smart_home.list_smart_devices())
    # List all smart homes of the user
    print("Smart homes of the user:")
    print(user.list_smart_homes())

