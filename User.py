import Network

# This code defines a User class that represents a user in a smart home system.
class User:
    _Users = 0
    def __init__(self, username):
        if username.lower() in ["example", "test", "admin"]:
            raise ValueError("Username exists in the system. Please choose a different username.")
        self.username = username
        self.network = None
        self.user_id = User._Users
        User._Users += 1

    # Magic Methods
    def __str__(self):
        return f"User: {self.username}"
    def __repr__(self):
        return f"User(username={self.username})"
    def __del__(self):
        print(f"User {self.username} has been removed from the system")

    # Connect and Disconnect from Network
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

    # Get User Count
    @classmethod
    def get_user_count(cls):
        return cls._Users

# This code defines a SmartHome class that represents a smart home in a network.
class SmartHome:
    _home_count = 0
    def __init__(self, network, name):
        self.smart_devices = []
        self.network = network
        self.name = name
        self.home_id = SmartHome._home_count
        if not isinstance(network, Network.Network):
            raise TypeError("Network must be an instance of Network class.")
        SmartHome._home_count += 1
        self.network.add_smart_home(self)

    # Magic Methods
    def __str__(self):
        return f"SmartHome: {self.name}, Network: {self.network.ip_address}"
    def __repr__(self):
        return f"SmartHome(name={self.name}, network={self.network.ip_address}, smart_devices={self.smart_devices})"
    def __del__(self):
        print(f"⚠️ SmartHome '{self.name}' has been removed from the system")
        print(f"  └─ Removing {len(self.smart_devices)} devices...")
        for smart_device in self.smart_devices:
            smart_device.__del__()
        self.smart_devices.clear()

    # Add and Remove Smart Devices
    def add_smart_device(self, smart_device):
        self.smart_devices.append(smart_device)
        print(f"✓ Added device '{smart_device.name}' to '{self.name}'")

    def remove_smart_device(self, smart_device):
        self.smart_devices.remove(smart_device)
        print(f"✓ Removed device '{smart_device.name}' from '{self.name}'")

    # List Smart Devices
    def list_smart_devices(self):
        return [smart_device for smart_device in self.smart_devices]

    # Security Assessment
    def secure_home(self):
        points = 0
        secure_types = ["Lock", "Security Camera", "Doorbell", "Door"]
        security_devices = []

        for device in self.smart_devices:
            if device.device_type in secure_types:
                security_devices.append(device)
                points += 1
                if device.is_on:
                    points += 1

        print(f"\n📊 Security Assessment for '{self.name}':")
        print(f"  ├─ Security devices: {len(security_devices)}/{len(self.smart_devices)}")
        print(f"  ├─ Active security devices: {sum(1 for d in security_devices if d.is_on)}/{len(security_devices)}")
        print(f"  └─ Security score: {points}/10")

        if points >= 6:
            print(f"  ✅ '{self.name}' is secure.")
        else:
            print(f"  ⚠️ '{self.name}' is not secure. Consider adding more security devices.")


    # Turn On/Off All Devices
    def turn_on_all_devices(self):
        print(f"📱 Turning on all devices in '{self.name}':")
        for device in self.smart_devices:
            device.turn_on()
            print(f"  ├─ {device.name}: ON")
        print(f"  └─ All {len(self.smart_devices)} devices activated.")
    def turn_off_all_devices(self):
        print(f"📱 Turning off all devices in '{self.name}':")
        for device in self.smart_devices:
            device.turn_off()
            print(f"  ├─ {device.name}: OFF")
        print(f"  └─ All {len(self.smart_devices)} devices deactivated.")

    # Get Energy Consumption
    def get_energy_consumption(self):
        total_consumption = sum(device.energy_consumption for device in self.smart_devices if device.is_on)
        active_devices = sum(1 for device in self.smart_devices if device.is_on)

        print(f"\n⚡ Energy consumption for '{self.name}':")
        print(f"  ├─ Active devices: {active_devices}/{len(self.smart_devices)}")
        print(f"  └─ Total consumption: {total_consumption:.2f} kWh")

        return total_consumption