from datetime import datetime, timedelta
from colorama import Fore, Style
import Network
import time as time_module
import threading

# Decorator to check if the device is ON before performing an operation
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

# This class represents a scheduled operation for a smart device.
class ScheduledOperation():
    def __init__(self, device_serial_number, operation, target_time, recurring, *args, **kwargs):
        self.recurring = recurring
        self.operation = operation
        self.target_time = target_time
        self.device_serial_number = device_serial_number
        self.args = args
        self.kwargs = kwargs
        SmartDevice.add_scheduled_operation(self)

    # Magic Methods
    def __str__(self):
        return f"ScheduledOperation(device={self.device_serial_number}, operation={self.operation}, target_time={self.target_time}, recurring={self.recurring})"
    def __repr__(self):
        return f"ScheduledOperation(device={self.device_serial_number}, operation={self.operation}, target_time={self.target_time}, recurring={self.recurring})"
    def __del__(self):
        print(Fore.RED + f"Scheduled operation for {self.device_serial_number} has been removed." + Style.RESET_ALL)
        try:
            SmartDevice._scheduled_operations.remove(self)
        except ValueError:
            print(Fore.YELLOW + f"Scheduled operation for {self.device_serial_number} was not found in the list." + Style.RESET_ALL)

    # Load the scheduled operation for a specific device
    def load(self, device):
        try:
            if not isinstance(device, SmartDevice):
                raise TypeError("Can only load scheduled operation for a SmartDevice instance.")
            else:
                print(f"Loading scheduled operation {self.operation} for {device.name} with serial number {device.serial_number}.")
            device.schedule_operation(self.operation, self.target_time, self.recurring, self, *self.args, **self.kwargs)
            #print(f"✓ Loaded scheduled operation {self.operation} for {device.name} at {self.target_time}.")
        except Exception as e:
            print(Fore.RED + f"Error loading scheduled operation: {e}" + Style.RESET_ALL)


# This code defines a SmartDevice class that represents a smart device in a smart home network.
class SmartDevice():
    _device_count = 0
    _scheduled_operations = []

    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.is_on = False
        self.energy_consumption = 3.5
        self.network = None
        self.serial_number = f"DEV-{SmartDevice._device_count}"
        SmartDevice._device_count += 1

    # Magic Methods
    def __str__(self):
        return f"{self.name} ({self.device_type}) - {'ON' if self.is_on else 'OFF'}"
    def __repr__(self):
        return f"SmartDevice(name={self.name}, device_type={self.device_type}, is_on={self.is_on})"
    def __del__(self):
        print(Fore.RED + f"SmartDevice {self.name} has been removed from the system" + Style.RESET_ALL)
        SmartDevice._device_count -= 1
        if self.network:
            print(f"  └─ Disconnecting from network at {self.network.ip_address}.")
            self.disconnect()
        print(f"  └─ Removing scheduled operations for {self.name}.")
        for operation in SmartDevice._scheduled_operations:
            if operation.device_serial_number == self.serial_number:
                operation.__del__()


    # Toggle the device state
    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    # Turn the device ON or OFF
    def turn_on(self):
        self.is_on = True
        print(f"{self.name} is now ON.")

    def turn_off(self):
        self.is_on = False
        print(f"{self.name} is now OFF.")

    # Set and get energy consumption
    def set_energy_consumption(self, consumption):
        self.energy_consumption = consumption
        print(f"{self.name} energy consumption set to {self.energy_consumption} kWh.")
    @is_on_check
    def get_energy_consumption(self):
        return self.energy_consumption

    # Connect and disconnect from a network
    def connect(self, network):
        if not isinstance(network, Network.Network):
            raise TypeError("Can only connect to a Network instance.")
        self.network = network
        print(f"✓ {self.name} has successfully connected to network at {network.ip_address}.")

    def disconnect(self):
        if self.network is None:
            print(f"! {self.name} is not currently connected to any network.")
            return
        old_network = self.network.ip_address
        self.network = None
        print(f"✓ {self.name} has disconnected from network at {old_network}.")

    # Set a delayed operation to be executed after a specific delay
    def delay_operation(self, operation, delay_seconds, recurring, sch_class, target_time, *args, **kwargs):
        if not hasattr(self, operation):
            print(f"Operation {operation} is not available for {self.name}.")
            return

        def delayed_operation():
            time_module.sleep(delay_seconds)
            try:
                getattr(self, operation)(*args, **kwargs)
                print(f"{operation} completed for {self.name} after {delay_seconds} seconds.")
            except Exception as e:
                print(f"Error during {operation} for {self.name}: {e}")
            if not recurring:
                print(SmartDevice._scheduled_operations)
                print(f"Removing scheduled operation {operation} for {self.name}.")
                # If not recurring, remove the operation from scheduled operations
                SmartDevice.remove_scheduled_operation(sch_class)
            else:
                print(f"Rescheduling {operation} for {self.name} every {target_time}.")
                # If recurring, reschedule the operation
                self.schedule_operation(operation, target_time, recurring, sch_class, *args, **kwargs)
        thread = threading.Thread(target=delayed_operation)
        thread.daemon = True
        thread.start()
        return thread

    # Schedule an operation to run at a specific time or after a delay.
    def schedule_operation(self, operation, target_time, recurring, sch_class, *args, **kwargs):
        if not hasattr(self, operation):
            print(f"Operation {operation} is not available for {self.name}.")
            return

        # Parse the time string
        try:
            # If target_time is already an int, treat it as seconds for backward compatibility
            if isinstance(target_time, int):
                return self.delay_operation(operation, target_time, recurring, sch_class, target_time, *args, **kwargs)

            # Parse the time string (format: "HH:MM")
            hour, minute = map(int, target_time.split(':'))
            now = datetime.now()
            target_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the time is already past for today, schedule it for tomorrow
            if target_datetime < now:
                target_datetime += timedelta(days=1)

            # Calculate seconds until the target time
            delay_seconds = (target_datetime - now).total_seconds()
            print(f"Scheduled {operation} for {self.name} at {target_time} (in {delay_seconds:.1f} seconds)")

            return self.delay_operation(operation, delay_seconds, recurring, sch_class, target_time, *args, **kwargs)
        except Exception as e:
            print(f"Error scheduling {operation}: {e}")
            print("Please provide time in HH:MM format (e.g., '14:30')")

    # Class methods to manage device count and scheduled operations
    @classmethod
    def get_device_count(cls):
        return cls._device_count

    @classmethod
    def get_scheduled_operations(cls):
        return cls._scheduled_operations

    @classmethod
    def add_scheduled_operation(cls, operation):
        if not isinstance(operation, ScheduledOperation):
            raise TypeError("Only scheduled_operation instances can be added.")
        cls._scheduled_operations.append(operation)
        print(f"Scheduled operation {operation} has been added for {operation.device_serial_number}.")

    @classmethod
    def remove_scheduled_operation(cls, operation):
        if not isinstance(operation, ScheduledOperation):
            raise TypeError("Only scheduled_operation instances can be removed.")
        try:
            cls._scheduled_operations.remove(operation)
            print(f"Scheduled operation {operation} has been removed.")
        except ValueError:
            print(f"Scheduled operation {operation} was not found in the list.")

    @classmethod
    def load_all_scheduled_operations(cls, device):
        if not isinstance(device, SmartDevice):
            raise TypeError("Can only load scheduled operations for a SmartDevice instance.")
        print(f"Loading all scheduled operations for {device.name} with serial number {device.serial_number}.")
        for operation in cls._scheduled_operations:
            if operation.device_serial_number == device.serial_number:
                operation.load(device)
                print(f"✓ Loaded scheduled operation {operation.operation} for {device.name} at {operation.target_time}.")

# Child class for a Smart Light
class SmartLight(SmartDevice):
    def __init__(self, name, brightness=50):
        super().__init__(name, "Light")
        self.brightness = brightness
        self.colour = "White"
        self.set_energy_consumption(0.5)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Light) - {'ON' if self.is_on else 'OFF'}, Brightness: {self.brightness}, Colour: {self.colour}"
    def __repr__(self):
        return f"SmartLight(name={self.name}, is_on={self.is_on}, brightness={self.brightness}, colour={self.colour})"

    # Methods to control the light
    @is_on_check
    def set_brightness(self, brightness):
        self.brightness = brightness
        print(f"{self.name} brightness set to {self.brightness}.")

    @is_on_check
    def set_colour(self, colour):
        self.colour = colour
        print(f"{self.name} colour set to {self.colour}.")

# Child class for a Smart Thermostat
class SmartThermostat(SmartDevice):
    def __init__(self, name, temperature=22):
        super().__init__(name, "Thermostat")
        self.temperature = temperature
        self.set_energy_consumption(3)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Thermostat) - {'ON' if self.is_on else 'OFF'}, Temperature: {self.temperature}"
    def __repr__(self):
        return f"SmartThermostat(name={self.name}, is_on={self.is_on}, temperature={self.temperature})"

    # Methods to control the thermostat
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

# Child class for a Smart Security Camera
class SmartCamera(SmartDevice):
    def __init__(self, name, resolution="1080p"):
        super().__init__(name, "Security Camera")
        self.resolution = resolution
        self.set_energy_consumption(10)
        self.recording = False

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Security Camera) - {'ON' if self.is_on else 'OFF'}, Resolution: {self.resolution}"
    def __repr__(self):
        return f"SmartSecurityCamera(name={self.name}, is_on={self.is_on}, resolution={self.resolution})"

    # Methods to control the camera
    @is_on_check
    def set_resolution(self, resolution):
        self.resolution = resolution
        print(f"{self.name} resolution set to {self.resolution}.")

    @is_on_check
    def record(self):
        if self.is_on:
            self.recording = True
            print(f"{self.name} is recording.")
        else:
            print(f"{self.name} is OFF. Cannot record.")

    @is_on_check
    def stop_recording(self):
        if self.is_on:
            self.recording = False
            print(f"{self.name} has stopped recording.")
        else:
            print(f"{self.name} is OFF. Cannot stop recording.")

    # Method to turn the camera OFF and stop recording
    def turn_off(self):
        self.stop_recording()
        super().turn_off()


# Child class for a Smart Appliance
class SmartAppliance(SmartDevice):
    def __init__(self, name, appliance_type):
        super().__init__(name, "Appliance")
        self.appliance_type = appliance_type
        self.set_energy_consumption(4)

    # Magic Methods
    def __str__(self):
        return f"{self.name} ({self.appliance_type}) - {'ON' if self.is_on else 'OFF'}"
    def __repr__(self):
        return f"SmartAppliance(name={self.name}, is_on={self.is_on}, appliance_type={self.appliance_type})"

    # Methods to control the appliance
    def set_appliance_type(self, appliance_type):
        self.appliance_type = appliance_type
        print(f"{self.name} appliance type set to {self.appliance_type}.")

# Child class for a Smart Speaker
class SmartSpeaker(SmartDevice):
    def __init__(self, name, volume=50):
        super().__init__(name, "Speaker")
        self.volume = volume
        self.song_playing = None
        self.set_energy_consumption(3)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Speaker) - {'ON' if self.is_on else 'OFF'}, Volume: {self.volume}"
    def __repr__(self):
        return f"SmartSpeaker(name={self.name}, is_on={self.is_on}, volume={self.volume})"

    # Methods to control the speaker
    @is_on_check
    def set_volume(self, volume):
        self.volume = volume
        print(f"{self.name} volume set to {self.volume}.")

    @is_on_check
    def increase_volume(self, amount):
        self.volume += amount
        print(f"{self.name} volume increased to {self.volume}.")

    @is_on_check
    def decrease_volume(self, amount):
        self.volume -= amount
        print(f"{self.name} volume decreased to {self.volume}.")

    @is_on_check
    def play_music(self, song):
        self.song_playing = song
        print(f"{self.name} is playing {song}.")

    @is_on_check
    def stop_music(self):
        self.song_playing = None
        print(f"{self.name} has stopped playing music.")

    def turn_off(self):
        self.stop_music()
        super().turn_off()

# Child class for Smart Lock
class SmartLock(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Lock")
        self.locked = True
        self.set_energy_consumption(1)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Lock) - {'LOCKED' if self.locked else 'UNLOCKED'}"
    def __repr__(self):
        return f"SmartLock(name={self.name}, is_on={self.is_on}, locked={self.locked})"

    # Methods to control the lock
    @is_on_check
    def lock(self):
        self.locked = True
        print(f"{self.name} is now LOCKED.")

    @is_on_check
    def unlock(self):
        self.locked = False
        print(f"{self.name} is now UNLOCKED.")

# Child class for Smart Doorbell
class SmartDoorbell(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Doorbell")
        self.ringing = False
        self.set_energy_consumption(10)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Doorbell) - {'RINGING' if self.ringing else 'NOT RINGING'}"
    def __repr__(self):
        return f"SmartDoorbell(name={self.name}, is_on={self.is_on}, ringing={self.ringing})"

    # Methods to control the doorbell
    @is_on_check
    def ring(self):
        self.ringing = True
        print(f"{self.name} is now RINGING.")

    @is_on_check
    def stop_ringing(self):
        self.ringing = False
        print(f"{self.name} has stopped RINGING.")

    def turn_off(self):
        self.stop_ringing()
        super().turn_off()


# Child class for Smart Door
class SmartDoor(SmartDevice):
    def __init__(self, name):
        super().__init__(name, "Door")
        self.open = False
        self.set_energy_consumption(15)

    # Magic Methods
    def __str__(self):
        return f"{self.name} (Door) - {'OPEN' if self.open else 'CLOSED'}"
    def __repr__(self):
        return f"SmartDoor(name={self.name}, is_on={self.is_on}, open={self.open})"

    # Methods to control the door
    @is_on_check
    def open_door(self):
        self.open = True
        print(f"{self.name} is now OPEN.")

    @is_on_check
    def close_door(self):
        self.open = False
        print(f"{self.name} is now CLOSED.")

