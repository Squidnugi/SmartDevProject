class Network:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.smart_homes = []

    def __str__(self):
        return f"Network: {self.ip_address}"
    def __repr__(self):
        return f"Network(ip_address={self.ip_address}, smart_homes={self.smart_homes})"
    def add_smart_home(self, smart_home):
        self.smart_homes.append(smart_home)
        print(f"{smart_home.name} has been added to the network {self.ip_address}.")
    def list_devices_in_network(self):
        for i in self.smart_homes:
            i.list_smart_devices()