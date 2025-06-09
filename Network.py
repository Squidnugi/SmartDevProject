
## This code defines a Network class that manages smart homes and their devices.
class Network:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.smart_homes = []
    # Magic Methods
    def __str__(self):
        return f"Network: {self.ip_address}"
    def __repr__(self):
        return f"Network(ip_address={self.ip_address}, smart_homes={self.smart_homes})"
    def __del__(self):
        print(f"Network {self.ip_address} has been removed from the system")
        print(f"  └─ Removing {len(self.smart_homes)} smart homes...")
        for smart_home in self.smart_homes:
            smart_home.__del__()
        self.smart_homes.clear()

    # Add and Remove Smart Homes
    def add_smart_home(self, smart_home):
        self.smart_homes.append(smart_home)
        print(f"{smart_home.name} has been added to the network {self.ip_address}.")
    def remove_smart_home(self, smart_home):
        self.smart_homes.remove(smart_home)
        print(f"{smart_home.name} has been removed from the network {self.ip_address}.")

    # List Smart Devices
    def list_smart_devices(self):
        devices = []
        for smart_home in self.smart_homes:
            devices.extend(smart_home.list_smart_devices())
        return devices

    # List Smart Homes
    def list_smart_homes(self):
        return self.smart_homes


