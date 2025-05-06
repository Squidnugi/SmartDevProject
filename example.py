from abc import ABC, abstractmethod
from colorama import Fore, Style


# Abstraction using Abstract Base Class
class Device(ABC):
    # Class variable
    device_count = 0

    def __init__(self, name):
        self.name = name  # Public attribute
        self._status = False  # Protected attribute (convention)
        self.__serial_number = f"DEV-{Device.device_count}"  # Private attribute
        Device.device_count += 1

    @abstractmethod
    def operate(self):
        """Abstract method that must be implemented by subclasses"""
        pass

    def __del__(self):
        # Destructor
        print(f"Device {self.name} has been removed from the system")

    @classmethod
    def get_device_count(cls):
        # Class method
        return cls.device_count

    @staticmethod
    def get_device_type_info():
        # Static method
        return "This is a smart home device"


# Base class for our inheritance hierarchy
class SmartDevice(Device):
    def __init__(self, name, location):
        super().__init__(name)
        self.location = location
        self._energy_usage = 0.0

    def operate(self):
        # Implementing the abstract method
        self._status = not self._status
        return f"{self.name} is now {'ON' if self._status else 'OFF'}"

    def get_serial(self):
        # Accessing private attribute with name mangling
        return self._Device__serial_number

    @property
    def status(self):
        # Encapsulation: getter property
        return "ON" if self._status else "OFF"

    @status.setter
    def status(self, value):
        # Encapsulation: setter property
        if isinstance(value, bool):
            self._status = value
        else:
            raise ValueError("Status must be boolean")


# First parent for multiple inheritance
class NetworkEnabled:
    def __init__(self, ip_address="192.168.1.1"):
        self.ip_address = ip_address
        self._connected = False

    def connect(self):
        self._connected = True
        return f"Connected to network at {self.ip_address}"

    def disconnect(self):
        self._connected = False
        return "Disconnected from network"

    @property
    def network_status(self):
        return "Connected" if self._connected else "Disconnected"


# Second parent for multiple inheritance
class VoiceActivated:
    def __init__(self, wake_word="Hey Assistant"):
        self.wake_word = wake_word

    def respond_to_voice(self, command):
        return f"Responding to: {command}"


# Inheritance
class SmartLight(SmartDevice):
    def __init__(self, name, location, brightness=50):
        super().__init__(name, location)
        self.brightness = brightness
        self.color = "White"

    def operate(self):
        # Polymorphism (method overriding)
        status = super().operate()
        return f"{status} with brightness {self.brightness}%"

    def dim(self, amount):
        self.brightness = max(0, self.brightness - amount)
        return f"{self.name} dimmed to {self.brightness}%"


class SmartThermostat(SmartDevice):
    def __init__(self, name, location, temperature=22):
        super().__init__(name, location)
        self.temperature = temperature

    def operate(self):
        # Polymorphism (method overriding)
        status = super().operate()
        return f"{status} at {self.temperature}°C"

    def adjust_temp(self, delta):
        self.temperature += delta
        return f"Temperature adjusted to {self.temperature}°C"


# Multiple Inheritance
class SmartSpeaker(SmartDevice, NetworkEnabled, VoiceActivated):
    def __init__(self, name, location, volume=50):
        SmartDevice.__init__(self, name, location)
        NetworkEnabled.__init__(self, "192.168.1.100")
        VoiceActivated.__init__(self, "Hey Speaker")
        self.volume = volume

    def operate(self):
        # Polymorphism
        status = SmartDevice.operate(self)
        if self._status:
            self.connect()
        else:
            self.disconnect()
        return f"{status} with volume {self.volume}% ({self.network_status})"


# Demonstration of all features
def main():
    # Create objects
    print(Fore.CYAN + "=== Creating smart devices ===" + Style.RESET_ALL)
    light = SmartLight("Bedroom Light", "Bedroom", 75)
    thermostat = SmartThermostat("Living Room Thermostat", "Living Room", 24)
    speaker = SmartSpeaker("Kitchen Speaker", "Kitchen", 60)

    # Demonstrate abstraction and polymorphism
    print(Fore.CYAN + "\n=== Demonstrating polymorphism with operate() method ===" + Style.RESET_ALL)
    print(light.operate())
    print(thermostat.operate())
    print(speaker.operate())

    # Demonstrate encapsulation
    print(Fore.CYAN + "\n=== Demonstrating encapsulation with properties ===" + Style.RESET_ALL)
    print(f"{light.name} status is {light.status}")
    light.status = False
    print(f"{light.name} status changed to {light.status}")

    # Demonstrate protected and private attributes
    print(Fore.CYAN + "\n=== Demonstrating access modifiers ===" + Style.RESET_ALL)
    print(f"Protected attribute access: light._status = {light._status}")
    # This wouldn't work directly: print(light.__serial_number)
    print(f"Private attribute accessed via method: {light.get_serial()}")

    # Demonstrate static and class methods
    print(Fore.CYAN + "\n=== Demonstrating static and class methods ===" + Style.RESET_ALL)
    print(f"Total devices: {Device.get_device_count()}")
    print(f"Device info: {Device.get_device_type_info()}")

    # Demonstrate multiple inheritance
    print(Fore.CYAN + "\n=== Demonstrating multiple inheritance ===" + Style.RESET_ALL)
    print(speaker.respond_to_voice("Play some music"))
    print(f"Speaker network status: {speaker.network_status}")
    print(f"Speaker wake word: {speaker.wake_word}")

    # Demonstrate class-specific methods
    print(Fore.CYAN + "\n=== Demonstrating class-specific methods ===" + Style.RESET_ALL)
    print(light.dim(25))
    print(thermostat.adjust_temp(2))

    # Demonstrate destructor (by removing reference)
    print(Fore.CYAN + "\n=== Demonstrating destructor ===" + Style.RESET_ALL)
    temp_device = SmartDevice("Temporary", "Hallway")
    print(f"Created {temp_device.name}")
    del temp_device  # This will trigger the destructor


if __name__ == "__main__":
    main()