from colorama import Fore, Style
import Network

def is_on_check(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not isinstance(instance, SmartDevice):
            raise TypeError("Decorator can only be applied to SmartDevice instances.")
        if not instance.is_on:
            print(Fore.RED + f"{instance.name} is OFF. Cannot perform the operation." + Style.RESET_ALL)
            return None
        result = func(*args, **kwargs)
        return result
    return wrapper

class SmartDevice():
    _device_count = 0
    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.is_on = False
        self.energy_consumption = 0.0
        self.network = None
        self.serial_number = f"DEV-{SmartDevice._device_count}"
        SmartDevice._device_count += 1

    def __str__(self):
        return f"{self.name} ({self.device_type}) - {'ON' if self.is_on else 'OFF'}"
    def __repr__(self):
        return f"SmartDevice(name={self.name}, device_type={self.device_type}, is_on={self.is_on})"
    def __del__(self):
        print(Fore.RED + f"SmartDevice {self.name} has been removed from the system" + Style.RESET_ALL)
        SmartDevice._device_count -= 1

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is now ON.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is now OFF.")

    def set_energy_consumption(self, consumption):
        self.energy_consumption = consumption
        print(f"{self.name} energy consumption set to {self.energy_consumption} kWh.")

    @is_on_check
    def get_energy_consumption(self):
        return self.energy_consumption

    def connect(self, network):
        if not isinstance(network, Network.Network):
            raise TypeError("Can only connect to a Network instance.")
        self.network = network
        print(f"{self.name} is now connected to {network.ip_address}.")


    @classmethod
    def get_device_count(cls):
        return cls._device_count


class SmartLight(SmartDevice):
    def __init__(self, name, brightness=50):
        super().__init__(name, "Light")
        self.brightness = brightness
        self.colour = "White"
    def __str__(self):
        return f"{self.name} (Light) - {'ON' if self.is_on else 'OFF'}, Brightness: {self.brightness}, Colour: {self.colour}"
    def __repr__(self):
        return f"SmartLight(name={self.name}, is_on={self.is_on}, brightness={self.brightness}, colour={self.colour})"

    @is_on_check
    def set_brightness(self, brightness):
        self.brightness = brightness
        print(f"{self.name} brightness set to {self.brightness}.")

    @is_on_check
    def set_colour(self, colour):
        self.colour = colour
        print(f"{self.name} colour set to {self.colour}.")


class SmartThermostat(SmartDevice):
    def __init__(self, name, temperature=22):
        super().__init__(name, "Thermostat")
        self.temperature = temperature
    def __str__(self):
        return f"{self.name} (Thermostat) - {'ON' if self.is_on else 'OFF'}, Temperature: {self.temperature}"
    def __repr__(self):
        return f"SmartThermostat(name={self.name}, is_on={self.is_on}, temperature={self.temperature})"

    @is_on_check
    def set_temperature(self, temperature):
        self.temperature = temperature
        print(f"{self.name} temperature set to {self.temperature}.")

    @is_on_check
    def increase_temperature(self, amount):
        self.temperature += amount
        print(f"{self.name} temperature increased to {self.temperature}.")

    @is_on_check
    def decrease_temperature(self, amount):
        self.temperature -= amount
        print(f"{self.name} temperature decreased to {self.temperature}.")

class SmartCamera(SmartDevice):
    def __init__(self, name, resolution="1080p"):
        super().__init__(name, "Security Camera")
        self.resolution = resolution
    def __str__(self):
        return f"{self.name} (Security Camera) - {'ON' if self.is_on else 'OFF'}, Resolution: {self.resolution}"
    def __repr__(self):
        return f"SmartSecurityCamera(name={self.name}, is_on={self.is_on}, resolution={self.resolution})"

    @is_on_check
    def set_resolution(self, resolution):
        self.resolution = resolution
        print(f"{self.name} resolution set to {self.resolution}.")

    @is_on_check
    def record(self):
        if self.is_on:
            print(f"{self.name} is recording.")
        else:
            print(f"{self.name} is OFF. Cannot record.")

    @is_on_check
    def stop_recording(self):
        if self.is_on:
            print(f"{self.name} has stopped recording.")
        else:
            print(f"{self.name} is OFF. Cannot stop recording.")

class SmartAppliance(SmartDevice):
    def __init__(self, name, appliance_type):
        super().__init__(name, appliance_type)
        self.appliance_type = appliance_type
    def __str__(self):
        return f"{self.name} ({self.appliance_type}) - {'ON' if self.is_on else 'OFF'}"
    def __repr__(self):
        return f"SmartAppliance(name={self.name}, is_on={self.is_on}, appliance_type={self.appliance_type})"

    def set_appliance_type(self, appliance_type):
        self.appliance_type = appliance_type
        print(f"{self.name} appliance type set to {self.appliance_type}.")


class SmartSpeaker(SmartDevice):
    def __init__(self, name, volume=50):
        super().__init__(name, "Speaker")
        self.volume = volume
    def __str__(self):
        return f"{self.name} (Speaker) - {'ON' if self.is_on else 'OFF'}, Volume: {self.volume}"
    def __repr__(self):
        return f"SmartSpeaker(name={self.name}, is_on={self.is_on}, volume={self.volume})"

    def set_volume(self, volume):
        self.volume = volume
        print(f"{self.name} volume set to {self.volume}.")

    def increase_volume(self, amount):
        self.volume += amount
        print(f"{self.name} volume increased to {self.volume}.")

    def decrease_volume(self, amount):
        self.volume -= amount
        print(f"{self.name} volume decreased to {self.volume}.")

    def play_music(self, song):
        if self.is_on:
            print(f"{self.name} is playing {song}.")
        else:
            print(f"{self.name} is OFF. Cannot play music.")

    def stop_music(self):
        if self.is_on:
            print(f"{self.name} has stopped playing music.")
        else:
            print(f"{self.name} is OFF. Cannot stop music.")

class SmartLock(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Lock")
        self.locked = True
    def __str__(self):
        return f"{self.name} (Lock) - {'LOCKED' if self.locked else 'UNLOCKED'}"
    def __repr__(self):
        return f"SmartLock(name={self.name}, is_on={self.is_on}, locked={self.locked})"

    def lock(self):
        self.locked = True
        print(f"{self.name} is now LOCKED.")

    def unlock(self):
        self.locked = False
        print(f"{self.name} is now UNLOCKED.")

class SmartDoorbell(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Doorbell")
        self.ringing = False
    def __str__(self):
        return f"{self.name} (Doorbell) - {'RINGING' if self.ringing else 'NOT RINGING'}"
    def __repr__(self):
        return f"SmartDoorbell(name={self.name}, is_on={self.is_on}, ringing={self.ringing})"

    def ring(self):
        self.ringing = True
        print(f"{self.name} is now RINGING.")

    def stop_ringing(self):
        self.ringing = False
        print(f"{self.name} has stopped RINGING.")

class SmartDoor(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Door")
        self.open = False
    def __str__(self):
        return f"{self.name} (Door) - {'OPEN' if self.open else 'CLOSED'}"
    def __repr__(self):
        return f"SmartDoor(name={self.name}, is_on={self.is_on}, open={self.open})"

    def open_door(self):
        self.open = True
        print(f"{self.name} is now OPEN.")

    def close_door(self):
        self.open = False
        print(f"{self.name} is now CLOSED.")

class SmartHub(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Hub")
        self.smart_devices = []
    def __str__(self):
        return f"{self.name} (Hub) - {'ON' if self.is_on else 'OFF'}"
    def __repr__(self):
        return f"SmartHub(name={self.name}, is_on={self.is_on}, smart_devices={self.smart_devices})"

    def add_device(self, device):
        self.smart_devices.append(device)
        print(f"{device.name} has been added to {self.name}.")

    def remove_device(self, device):
        self.smart_devices.remove(device)
        print(f"{device.name} has been removed from {self.name}.")

    def list_devices(self):
        return [device.name for device in self.smart_devices]