import Network

#each home is connected to a IP address and when a user connects to that IP address, they can access the smart devices in that home
class User:
    def __init__(self, username):
        if username.lower() in ["example", "test", "admin"]:
            raise ValueError("Username exists in the system. Please choose a different username.")
        self.username = username
        self.network = None

    def __str__(self):
        return f"User: {self.username}"
    def __repr__(self):
        return f"User(username={self.username})"
    def __del__(self):
        print(f"User {self.username} has been removed from the system")


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
        self.smart_hubs = []
        self.smart_devices = []
        self.network = network
        self.name = name
    def __str__(self):
        return f"SmartHome: {self.name}, Network: {self.network.ip_address}"
    def __repr__(self):
        return f"SmartHome(name={self.name}, network={self.network.ip_address}, smart_hubs={self.smart_hubs}, smart_devices={self.smart_devices})"
    def __del__(self):
        print(f"SmartHome {self.name} has been removed from the system")
        for smart_hub in self.smart_hubs:
            smart_hub.__del__()
        for smart_device in self.smart_devices:
            smart_device.__del__()
        self.smart_hubs.clear()
        self.smart_devices.clear()

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

    def secure_home(self):
        points = 0
        secure_types = ["Lock", "Camera", "Doorbell", "Door"]
        for device in self.smart_devices:
            if device.device_type in secure_types:
                points += 1
                if device.is_on:
                    points += 1
        if points >= 6:
            print(f"{self.name} is secure.")
        else:
            print(f"{self.name} is not secure. Points: {points}")