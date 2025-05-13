class Network:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def __str__(self):
        return f"Network: {self.ip_address}"
    def __repr__(self):
        return f"Network(ip_address={self.ip_address}, smart_homes={self.smart_homes})"

