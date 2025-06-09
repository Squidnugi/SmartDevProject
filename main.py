from colorama import Fore, Style
import SmartDevice
import time
import Network
import User
import pickle

# This is the main GUI class that handles user interactions and displays menus
class GUI():
    def __init__(self):
        self.users = []
        self.networks = []
        self.logged_in_user = None
        self.connected_network = None
        self.scheduled_operations = []
        self.device_count = 0
        self.user_count = 0

    # Add a user to the GUI
    def add_user(self, user):
        self.users.append(user)

    # Add a network to the GUI
    def add_network(self, network):
        self.networks.append(network)

    # Set the currently logged-in user
    def set_logged_in_user(self, user):
        self.logged_in_user = user

    # Set the currently connected network
    def set_connected_network(self, network):
        self.connected_network = network

    # Display functions

    # Display a header for the menu or section
    def display_header(self, title):
        print("\n" + "═" * 50)
        print(f"{Fore.CYAN}■ {title}{Style.RESET_ALL}")
        print("═" * 50)

    # Display menu options in a consistent format
    def display_menu_options(self, options):
        """Display menu options in a consistent format"""
        for idx, option in options.items():
            print(f"  {Fore.YELLOW}[{idx}]{Style.RESET_ALL} {option}")
        print("─" * 50)

    # Display messages in a consistent format
    def display_success(self, message):
        """Display success messages in a consistent format"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

    # Display error messages in a consistent format
    def display_error(self, message):
        """Display error messages in a consistent format"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

    # Display warning messages in a consistent format
    def display_warning(self, message):
        """Display warning messages in a consistent format"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

    # Display info messages in a consistent format
    def display_info(self, message):
        """Display info messages in a consistent format"""
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

    # Prompt user for input with consistent formatting
    def prompt(self, message):
        """Prompt user for input with consistent formatting"""
        return input(f"{Fore.CYAN}► {message}: {Style.RESET_ALL}")

    # Main Menu for when no user logged in
    def logged_out(self):
        self.display_header("SMART HOME SYSTEM LOGIN")

        options = {
            "1": "Create a new user",
            "2": "Log in",
            "3": "Exit"
        }
        self.display_menu_options(options)

        choice = self.prompt("Enter your choice")

        # Create new User
        if choice == "1":
            username = self.prompt("Enter a username")
            user = next((user for user in self.users if user.username == username), None)
            if user:
                self.display_error(f"Username '{username}' already exists")
                return False
            try:
                self.logged_in_user = User.User(username)
                if self.connected_network is not None:
                    self.logged_in_user.connect_to_network(self.connected_network)
                self.users.append(self.logged_in_user)
                self.display_success(f"User '{username}' created successfully!")
                return False
            except ValueError as e:
                self.display_error(str(e))
                return False

        # Log in existing User
        elif choice == "2":
            username = self.prompt("Enter your username")
            user = next((user for user in self.users if user.username == username), None)
            if user:
                self.logged_in_user = user
                if self.connected_network is not None:
                    try:
                        self.logged_in_user.connect_to_network(self.connected_network)
                    except ValueError as e:
                        self.display_error(str(e))
                        return False
                self.display_success(f"Welcome back, {username}!")
                return False
            else:
                self.display_error("User not found. Please create a new user.")
                return False

        # Exit the system
        elif choice == "3":
            self.display_info("Exiting the system.")
            return True

        # Invalid choice
        else:
            self.display_warning("Invalid choice. Please try again.")
            return False

    # Main Menu for when user logged in
    def logged_in(self):
        time.sleep(1)
        self.display_header("SMART HOME CONTROL PANEL")

        # Options based on whether user is connected to a network
        if self.connected_network is not None:
            self.display_info(f"Connected to network: {self.connected_network.ip_address}")
            options = {
                "1": "Create a new smart home",
                "2": "Select a smart home",
                "3": "List smart homes",
                "4": "Create a new device",
                "5": "List devices in network",
                "6": "Select a device",
                "7": "Select Network",
                "0": "Log out"
            }
        else:
            options = {
                "1": "Connect to Network",
                "0": "Log out"
            }
        self.display_menu_options(options)

        choice = self.prompt("Enter your choice")

        # Create a new smart home
        if choice == "1" and self.connected_network is not None:
            name = self.prompt("Enter a name for your smart home")
            smart_home = User.SmartHome(self.logged_in_user.network, name)
            self.display_success(f"Smart home '{name}' created successfully!")

        # Select a smart home
        elif choice == "2" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                self.display_error("No smart homes found. Please create a smart home first.")
                return False

            self.display_info("Available Smart Homes:")
            for i, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

            smart_home_idx = self.prompt("Enter the number of the smart home")
            try:
                idx = int(smart_home_idx) - 1
                if 0 <= idx < len(self.connected_network.smart_homes):
                    smart_home = self.connected_network.smart_homes[idx]
                    self.display_success(f"Selected smart home: {smart_home.name}")
                    self.home_details(smart_home)
                else:
                    self.display_error("Invalid smart home number.")
            except ValueError:
                self.display_error("Please enter a valid number.")

        # List smart homes
        elif choice == "3" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                self.display_error("No smart homes found.")
                return False
            self.display_info("Smart Homes in Network:")
            for i, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

        # Create a new device
        elif choice == "4" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                self.display_error("No smart homes found. Please create a smart home first.")
                return False

            name = self.prompt("Enter a name for your device")

            device_types = {
                "1": "Light",
                "2": "Thermostat",
                "3": "Camera",
                "4": "Lock",
                "5": "Speaker",
                "6": "Doorbell",
                "7": "Door",
                "8": "Appliance",
                "9": "Custom"
            }

            self.display_info("Available Device Types:")
            self.display_menu_options(device_types)

            device_type_choice = self.prompt("Select device type")
            device_type = device_types.get(device_type_choice)

            if device_type == "Custom":
                device_type = self.prompt("Enter the type of device")

            self.display_info("Available Smart Homes:")
            for i, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

            smart_home_idx = self.prompt("Enter the number of the smart home")
            try:
                idx = int(smart_home_idx) - 1
                if 0 <= idx < len(self.connected_network.smart_homes):
                    smart_home = self.connected_network.smart_homes[idx]

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
                        device = SmartDevice.SmartAppliance(name, "Generic Appliance")
                    else:
                        device = SmartDevice.SmartDevice(name, device_type)

                    smart_home.add_smart_device(device)
                    self.display_success(f"Device '{name}' added to '{smart_home.name}' successfully!")
                else:
                    self.display_error("Invalid smart home number.")
            except ValueError:
                self.display_error("Please enter a valid number.")

        # List devices in network
        elif choice == "5" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                self.display_error("No smart homes found. Please create a smart home first.")
                return False

            self.display_info("Devices in Network:")
            for i, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  {Fore.BLUE}■ Smart Home: {home.name}{Style.RESET_ALL}")
                if not home.smart_devices:
                    print(f"    {Fore.YELLOW}No devices in this home{Style.RESET_ALL}")
                for j, device in enumerate(home.smart_devices, 1):
                    status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if device.is_on else f"{Fore.RED}OFF{Style.RESET_ALL}"
                    print(f"    {Fore.YELLOW}[{j}]{Style.RESET_ALL} {device.name} ({device.device_type}) - {status}")

        # Select a device
        elif choice == "6" and self.connected_network is not None:
            if not self.connected_network.smart_homes:
                self.display_error("No smart homes found. Please create a smart home first.")
                return False

            self.display_info("Available Smart Homes:")
            for i, home in enumerate(self.connected_network.smart_homes, 1):
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

            try:
                home_idx = int(self.prompt("Select a smart home by number")) - 1
                if 0 <= home_idx < len(self.connected_network.smart_homes):
                    smart_home = self.connected_network.smart_homes[home_idx]
                else:
                    self.display_error("Invalid smart home number.")
                    return False
            except ValueError:
                self.display_error("Please enter a valid number.")
                return False

            if not smart_home.smart_devices:
                self.display_error(f"No devices found in '{smart_home.name}'.")
                return False

            self.display_info(f"Devices in '{smart_home.name}':")
            for i, device in enumerate(smart_home.smart_devices, 1):
                status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if device.is_on else f"{Fore.RED}OFF{Style.RESET_ALL}"
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {device.name} ({device.device_type}) - {status}")

            try:
                device_idx = int(self.prompt("Select a device by number")) - 1
                if 0 <= device_idx < len(smart_home.smart_devices):
                    device = smart_home.smart_devices[device_idx]
                    self.display_success(f"Selected device: {device.name}")
                    self.device_details(device, smart_home)
                else:
                    self.display_error("Invalid device number.")
            except ValueError:
                self.display_error("Please enter a valid number.")

        # Select Network
        elif choice == "7" and self.connected_network is not None:
            self.network_details()

        # Log out
        elif choice == "0":
            self.display_info(f"Logging out {self.logged_in_user.username}...")
            if self.connected_network is not None:
                self.logged_in_user.disconnect_from_network()
                self.set_connected_network(None)
            self.set_logged_in_user(None)


        # Connect to Network
        elif choice == "1" and self.connected_network is None:
            if not self.networks:
                self.display_error("No networks available.")
                return False

            self.display_info("Available Networks:")
            for i, network in enumerate(self.networks, 1):
                print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {network.ip_address}")

            try:
                network_idx = int(self.prompt("Select a network by number")) - 1
                if 0 <= network_idx < len(self.networks):
                    network = self.networks[network_idx]
                    try:
                        self.logged_in_user.connect_to_network(network)
                        self.connected_network = network
                        self.display_success(f"Connected to network: {network.ip_address}")
                    except ValueError as e:
                        self.display_error(str(e))
                else:
                    self.display_error("Invalid network number.")
            except ValueError:
                self.display_error("Please enter a valid number.")

        # Invalid choice
        else:
            self.display_warning("Invalid choice. Please try again.")

        return False

    # Home Details Menu
    def device_details(self, device, home):
        while True:
            self.display_header(f"DEVICE: {device.name} ({device.device_type})")
            status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if device.is_on else f"{Fore.RED}OFF{Style.RESET_ALL}"
            print(f"Status: {status}")

            options = {
                "1": "Turn on/off device",
                "2": "Get device status",
                "3": "Schedule operation",
                "4": "Device operations",
                "5": "View scheduled operations",
                "6": "Delete device",
                "7": "Back to main menu"
            }
            self.display_menu_options(options)

            choice = self.prompt("Enter your choice")

            # Toggle device on/off
            if choice == "1":
                device.toggle()
                status = "ON" if device.is_on else "OFF"
                self.display_success(f"Device {device.name} turned {status}")

            # Display device information
            elif choice == "2":
                self.display_info(f"Device Information:")
                print(f"  ┌─ Serial Number: {device.serial_number}")
                print(f"  ├─ Name: {device.name}")
                print(f"  ├─ Type: {device.device_type}")
                print(f"  ├─ Status: {'On' if device.is_on else 'Off'}")
                if hasattr(device, 'brightness'):
                    print(f"  ├─ Brightness: {device.brightness}%")
                if hasattr(device, 'colour'):
                    print(f"  ├─ Colour: {device.colour}")
                if hasattr(device, 'temperature'):
                    print(f"  ├─ Temperature: {device.temperature}°C")
                if hasattr(device, 'resolution'):
                    print(f"  ├─ Resolution: {device.resolution}")
                if hasattr(device, 'volume'):
                    print(f"  ├─ Volume: {device.volume}%")
                if hasattr(device, 'locked'):
                    print(f"  ├─ Lock Status: {'Locked' if device.locked else 'Unlocked'}")
                if hasattr(device, 'open'):
                    print(f"  ├─ Door Status: {'Open' if device.open else 'Closed'}")
                if hasattr(device, 'recording'):
                    print(f"  ├─ Recording Status: {'Recording' if device.recording_status else 'Not Recording'}")
                if hasattr(device, 'appliance_type'):
                    print(f"  ├─ Appliance Type: {device.appliance_type}")
                if hasattr(device, 'ringing'):
                    print(f"  ├─ Ringing Status: {'Ringing' if device.ringing else 'Not Ringing'}")
                print(f"  └─ Energy: {device.energy_consumption} kWh")

            # Schedule an operation
            elif choice == "3":
                self.schedule_device_operation(device, home)

            # Device operations menu
            elif choice == "4":
                self.device_operations(device)

            # View scheduled operations
            elif choice == "5":
                operations = SmartDevice.SmartDevice.get_scheduled_operations()
                if operations:
                    self.display_info("Scheduled Operations:")
                    options = {}
                    loop = 1
                    for op in operations:
                        if op.device_serial_number == device.serial_number:
                            # Format the target_time string properly
                            device_info = f"Device: {op.device_serial_number}"
                            function_info = f"operation: {op.operation}"
                            recurring = "Recurring" if op.recurring else "One-time"

                            # Add to options dictionary
                            options[str(loop)] = f"{op.target_time} - {device_info} - {function_info} ({recurring})"
                            loop+=1

                    options["0"] = "Back to device menu"
                    self.display_menu_options(options)

                    op_choice = self.prompt("Select an operation to view details or 0 to exit")

                    # Check if the user wants to exit or view details
                    if op_choice == "0":
                        pass
                    else:
                        try:
                            idx = int(op_choice) - 1
                            if 0 <= idx < len(operations):
                                selected_op = operations[idx]
                                self.display_header("OPERATION DETAILS")
                                print(f"Device Serial: {selected_op.device_serial_number}")
                                print(f"Operation: {selected_op.operation}")
                                print(f"Scheduled Time: {selected_op.target_time}")
                                print(f"Recurring: {'Yes' if selected_op.recurring else 'No'}")

                                # Show arguments if any
                                if hasattr(selected_op, 'args') and selected_op.args:
                                    print("Arguments:")
                                    for arg in selected_op.args:
                                        print(f"  - {arg}")

                                # Option to delete the scheduled operation
                                delete = self.prompt(
                                    "Would you like to delete this operation? (yes/no)").strip().lower()
                                if delete == "yes":
                                    operations.remove(selected_op)
                                    self.display_success("Operation removed successfully!")
                            else:
                                self.display_error("Invalid operation number.")
                        except ValueError:
                            self.display_error("Please enter a valid number.")
                else:
                    self.display_info("No scheduled operations.")

            # Delete the device
            elif choice == "6":
                confirm = self.prompt("Are you sure you want to delete this device? (yes/no)").strip().lower()
                if confirm == "yes":
                    try:
                        home.remove_smart_device(device)
                        self.display_success(f"Device '{device.name}' deleted successfully!")
                        break
                    except ValueError as e:
                        self.display_error(str(e))
                else:
                    self.display_info("Device deletion cancelled.")

            # Back to main menu
            elif choice == "7":
                break

            # Invalid choice
            else:
                self.display_warning("Invalid choice. Please try again.")

    # Device Schedule Operations
    def schedule_device_operation(self, device, home):
        self.display_header(f"SCHEDULE OPERATION FOR {device.name}")

        # Get the time to schedule
        scheduled_time = self.prompt("Enter the time to schedule the operation (HH:MM)")
        # Calculate minutes until the scheduled time
        try:
            now = time.localtime()
            hour, minute = map(int, scheduled_time.split(":"))
            scheduled = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday, hour, minute, 0, now.tm_wday, now.tm_yday, now.tm_isdst))
            scheduled_timestamp = time.mktime(scheduled)
            now_timestamp = time.mktime(now)
            if scheduled_timestamp < now_timestamp:
                # If the time is earlier than now, schedule for the next day
                scheduled = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday + 1, hour, minute, 0, (now.tm_wday + 1) % 7, now.tm_yday + 1, now.tm_isdst))
                scheduled_timestamp = time.mktime(scheduled)
            minutes = int((scheduled_timestamp - now_timestamp) // 60)
        except Exception:
            self.display_error("Invalid time format. Please use HH:MM.")
            return

        self.display_info(f"Select operation to schedule for {device.name}:")

        # Define operations based on device type
        if isinstance(device, SmartDevice.SmartLight):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set brightness",
                "4": "Set colour"
            }
        elif isinstance(device, SmartDevice.SmartThermostat):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set temperature",
                "4": "Increase temperature",
                "5": "Decrease temperature"
            }
        elif isinstance(device, SmartDevice.SmartCamera):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Record",
                "4": "Stop recording",
                "5": "Set resolution"
            }
        elif isinstance(device, SmartDevice.SmartLock):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Lock",
                "4": "Unlock"
            }
        elif isinstance(device, SmartDevice.SmartSpeaker):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set volume",
                "4": "Increase volume",
                "5": "Decrease volume",
                "6": "Play music",
                "7": "Stop music"
            }
        elif isinstance(device, SmartDevice.SmartDoorbell):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Ring",
                "4": "Stop ringing"
            }
        elif isinstance(device, SmartDevice.SmartDoor):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Open door",
                "4": "Close door"
            }
        else:
            options = {
                "1": "Turn on",
                "2": "Turn off"
            }

        options["0"] = "Cancel scheduling"
        self.display_menu_options(options)

        choice = self.prompt("Select operation to schedule")

        # Common operations
        if choice == "1":
            temp_sch = SmartDevice.scheduled_operation(device.serial_number, "turn_on", scheduled_time, False)
            self.display_success(f"Scheduled {device.name} to turn ON in {minutes} minutes")
        elif choice == "2":
            temp_sch = SmartDevice.scheduled_operation(device.serial_number, "turn_off", scheduled_time, False)
            self.display_success(f"Scheduled {device.name} to turn OFF in {minutes} minutes")
        elif choice == "0":
            self.display_info("Scheduling cancelled")
            return

        # Device specific operations
        elif choice == "3":
            if isinstance(device, SmartDevice.SmartLight):
                try:
                    brightness = int(self.prompt("Enter brightness level (0-100)"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "set_brightness", scheduled_time, False, brightness)
                    self.display_success(
                        f"Scheduled {device.name} brightness to set to {brightness} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartThermostat):
                try:
                    temp = float(self.prompt("Enter temperature"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "set_temperature", scheduled_time, False)
                    self.display_success(f"Scheduled {device.name} temperature to set to {temp} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid temperature")
            elif isinstance(device, SmartDevice.SmartCamera):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "record", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to start recording in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartLock):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "lock", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to lock in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    volume = int(self.prompt("Enter volume level (0-100)"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "set_volume", scheduled_time, False, volume)
                    self.display_success(f"Scheduled {device.name} volume to set to {volume} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartDoorbell):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "ring", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to ring in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartDoor):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "open_door", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to open in {minutes} minutes")
            else:
                self.display_error("Invalid operation for this device type")
                return

        elif choice == "4":
            if isinstance(device, SmartDevice.SmartLight):
                colour = self.prompt("Enter colour")
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "set_colour", scheduled_time, False, colour)
                self.display_success(f"Scheduled {device.name} colour to set to {colour} in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartThermostat):
                try:
                    amount = float(self.prompt("Enter amount to increase"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "increase_temperature", scheduled_time, False, amount)
                    self.display_success(
                        f"Scheduled {device.name} temperature to increase by {amount} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartCamera):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "stop_recording", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to stop recording in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartLock):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "unlock", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to unlock in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    amount = int(self.prompt("Enter amount to increase"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "increase_volume", scheduled_time, False, amount)
                    self.display_success(f"Scheduled {device.name} volume to increase by {amount} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartDoorbell):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "stop_ringing", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to stop ringing in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartDoor):
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "close_door", scheduled_time, False)
                self.display_success(f"Scheduled {device.name} to close in {minutes} minutes")
            else:
                self.display_error("Invalid operation for this device type")
                return

        elif choice == "5":
            if isinstance(device, SmartDevice.SmartThermostat):
                try:
                    amount = float(self.prompt("Enter amount to decrease"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "decrease_temperature", scheduled_time, False, amount)
                    self.display_success(f"Scheduled {device.name} temperature to decrease by {amount} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartCamera):
                resolution = self.prompt("Enter resolution (e.g. 1080p)")
                temp_sch = SmartDevice.scheduled_operation(device.serial_number, "set_resolution", scheduled_time, False, resolution)
                self.display_success(f"Scheduled {device.name} resolution to set to {resolution} in {minutes} minutes")
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    amount = int(self.prompt("Enter amount to decrease"))
                    temp_sch = SmartDevice.scheduled_operation(device.serial_number, "decrease_volume", scheduled_time, False, amount)
                    self.display_success(f"Scheduled {device.name} volume to decrease by {amount} in {minutes} minutes")
                except ValueError:
                    self.display_error("Please enter a valid number")
            else:
                self.display_error("Invalid operation for this device type")
                return

        elif choice == "6" and isinstance(device, SmartDevice.SmartSpeaker):
            song = self.prompt("Enter name of song to play")
            temp_sch = SmartDevice.scheduled_operation(device.serial_number, "play_music", scheduled_time, False, song)
            self.display_success(f"Scheduled {device.name} to play '{song}' in {minutes} minutes")

        elif choice == "7" and isinstance(device, SmartDevice.SmartSpeaker):
            temp_sch = SmartDevice.scheduled_operation(device.serial_number, "stop_music", scheduled_time, False)
            self.display_success(f"Scheduled {device.name} to stop music in {minutes} minutes")

        # Invalid choice
        else:
            self.display_error("Invalid choice. Please try again.")
            return

        recurring = self.prompt("Is this a recurring operation? (yes/no)").strip().lower()
        # Validate recurring input
        if recurring == "yes":
            # Schedule the recurring operation
            temp_sch.recurring = True
            self.display_success(f"Recurring operation scheduled")
        elif recurring == "no":
            temp_sch.recurring = False
            self.display_success("Non-recurring operation scheduled successfully")
        else:
            self.display_error("Invalid input. Set to non-recurring by default.")
        temp_sch.load(device)

    # Device Operations Menu
    def device_operations(self, device):
        self.display_header(f"OPERATIONS FOR {device.name}")

        # Define operations based on device type
        if isinstance(device, SmartDevice.SmartLight):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set brightness",
                "4": "Set colour"
            }
        elif isinstance(device, SmartDevice.SmartThermostat):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set temperature",
                "4": "Increase temperature",
                "5": "Decrease temperature"
            }
        elif isinstance(device, SmartDevice.SmartCamera):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Record",
                "4": "Stop recording",
                "5": "Set resolution"
            }
        elif isinstance(device, SmartDevice.SmartLock):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Lock",
                "4": "Unlock"
            }
        elif isinstance(device, SmartDevice.SmartSpeaker):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Set volume",
                "4": "Increase volume",
                "5": "Decrease volume",
                "6": "Play music",
                "7": "Stop music"
            }
        elif isinstance(device, SmartDevice.SmartDoorbell):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Ring",
                "4": "Stop ringing"
            }
        elif isinstance(device, SmartDevice.SmartDoor):
            options = {
                "1": "Turn on",
                "2": "Turn off",
                "3": "Open door",
                "4": "Close door"
            }
        else:
            options = {
                "1": "Turn on",
                "2": "Turn off"
            }

        options["0"] = "Back to device menu"
        self.display_menu_options(options)

        choice = self.prompt("Select operation")

        # Common operations
        if choice == "1":
            device.turn_on()
            self.display_success(f"{device.name} turned ON")
        elif choice == "2":
            device.turn_off()
            self.display_success(f"{device.name} turned OFF")
        elif choice == "0":
            return

        # Device specific operations
        elif choice == "3":
            if isinstance(device, SmartDevice.SmartLight):
                try:
                    brightness = int(self.prompt("Enter brightness level (0-100)"))
                    device.set_brightness(brightness)
                    self.display_success(f"Brightness set to {brightness}")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartThermostat):
                try:
                    temp = float(self.prompt("Enter temperature"))
                    device.set_temperature(temp)
                    self.display_success(f"Temperature set to {temp}")
                except ValueError:
                    self.display_error("Please enter a valid temperature")
            elif isinstance(device, SmartDevice.SmartCamera):
                device.record()
            elif isinstance(device, SmartDevice.SmartLock):
                device.lock()
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    volume = int(self.prompt("Enter volume level (0-100)"))
                    device.set_volume(volume)
                    self.display_success(f"Volume set to {volume}")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartDoorbell):
                device.ring()
            elif isinstance(device, SmartDevice.SmartDoor):
                device.open_door()

        elif choice == "4":
            if isinstance(device, SmartDevice.SmartLight):
                colour = self.prompt("Enter colour")
                device.set_colour(colour)
                self.display_success(f"Colour set to {colour}")
            elif isinstance(device, SmartDevice.SmartThermostat):
                try:
                    amount = float(self.prompt("Enter amount to increase"))
                    device.increase_temperature(amount)
                    self.display_success(f"Temperature increased by {amount}")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartCamera):
                device.stop_recording()
            elif isinstance(device, SmartDevice.SmartLock):
                device.unlock()
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    amount = int(self.prompt("Enter amount to increase"))
                    device.increase_volume(amount)
                    self.display_success(f"Volume increased by {amount}")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartDoorbell):
                device.stop_ringing()
            elif isinstance(device, SmartDevice.SmartDoor):
                device.close_door()

        elif choice == "5":
            if isinstance(device, SmartDevice.SmartThermostat):
                try:
                    amount = float(self.prompt("Enter amount to decrease"))
                    device.decrease_temperature(amount)
                    self.display_success(f"Temperature decreased by {amount}")
                except ValueError:
                    self.display_error("Please enter a valid number")
            elif isinstance(device, SmartDevice.SmartCamera):
                resolution = self.prompt("Enter resolution (e.g. 1080p)")
                device.set_resolution(resolution)
                self.display_success(f"Resolution set to {resolution}")
            elif isinstance(device, SmartDevice.SmartSpeaker):
                try:
                    amount = int(self.prompt("Enter amount to decrease"))
                    device.decrease_volume(amount)
                    self.display_success(f"Volume decreased by {amount}")
                except ValueError:
                    self.display_error("Please enter a valid number")

        elif choice == "6" and isinstance(device, SmartDevice.SmartSpeaker):
            song = self.prompt("Enter name of song to play")
            device.play_music(song)

        elif choice == "7" and isinstance(device, SmartDevice.SmartSpeaker):
            device.stop_music()

        # Invalid choice
        else:
            self.display_warning("Invalid choice or operation not available for this device type.")

    # Smart Home Details Menu
    def home_details(self, home):
        while True:
            self.display_header(f"SMART HOME: {home.name}")

            options = {
                "1": "List devices",
                "2": "Secure home",
                "3": "Energy consumption",
                "4": "Turn all devices ON",
                "5": "Turn all devices OFF",
                "6": "Delete home",
                "7": "Back to main menu"
            }
            self.display_menu_options(options)

            choice = self.prompt("Enter your choice")

            # List devices in the home
            if choice == "1":
                self.display_info(f"Devices in '{home.name}':")
                if not home.smart_devices:
                    print(f"  {Fore.YELLOW}No devices found{Style.RESET_ALL}")
                for i, device in enumerate(home.smart_devices, 1):
                    status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if device.is_on else f"{Fore.RED}OFF{Style.RESET_ALL}"
                    print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {device.name} ({device.device_type}) - {status}")

            # Secure the home
            elif choice == "2":
                home.secure_home()

            # Get energy consumption of the home
            elif choice == "3":
                home.get_energy_consumption()

            # Turn on all devices in the home
            elif choice == "4":
                home.turn_on_all_devices()

            # Turn off all devices in the home
            elif choice == "5":
                home.turn_off_all_devices()

            # Delete the home
            elif choice == "6":
                confirm = self.prompt("Are you sure you want to delete this home? (yes/no)").strip().lower()
                if confirm == "yes":
                    try:
                        self.connected_network.remove_smart_home(home)
                        self.display_success(f"Smart home '{home.name}' deleted successfully!")
                        break
                    except ValueError as e:
                        self.display_error(str(e))
                else:
                    self.display_info("Home deletion cancelled.")

            # Back to main menu
            elif choice == "7":
                break

            # Invalid choice
            else:
                self.display_warning("Invalid choice. Please try again.")

    # Network Details Menu
    def network_details(self):
        while True:
            self.display_header(f"NETWORK: {self.connected_network.ip_address}")

            options = {
                "1": "List smart homes",
                "2": "Add smart home",
                "3": "Remove smart home",
                "4": "List all devices",
                "5": "Disconnect from network",
                "6": "Back to main menu"
            }
            self.display_menu_options(options)

            choice = self.prompt("Enter your choice")

            # List smart homes in the network
            if choice == "1":
                self.display_info(f"Smart homes in network {self.connected_network.ip_address}:")
                if not self.connected_network.smart_homes:
                    print(f"  {Fore.YELLOW}No smart homes found{Style.RESET_ALL}")
                for i, home in enumerate(self.connected_network.smart_homes, 1):
                    print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

            # Add a new smart home to the network
            elif choice == "2":
                name = self.prompt("Enter a name for the smart home")
                smart_home = User.SmartHome(self.connected_network, name)
                self.display_success(f"Smart home '{name}' added successfully!")

            # Remove a smart home from the network
            elif choice == "3":
                if not self.connected_network.smart_homes:
                    self.display_error("No smart homes found.")
                    return

                self.display_info("Available Smart Homes:")
                for i, home in enumerate(self.connected_network.smart_homes, 1):
                    print(f"  {Fore.YELLOW}[{i}]{Style.RESET_ALL} {home.name}")

                try:
                    home_idx = int(self.prompt("Select a smart home to remove")) - 1
                    if 0 <= home_idx < len(self.connected_network.smart_homes):
                        smart_home = self.connected_network.smart_homes[home_idx]
                        confirm = self.prompt(
                            f"Are you sure you want to remove '{smart_home.name}'? (yes/no)").strip().lower()
                        if confirm == "yes":
                            self.connected_network.remove_smart_home(smart_home)
                            self.display_success(f"Smart home '{smart_home.name}' removed successfully!")
                        else:
                            self.display_info("Home removal cancelled.")
                    else:
                        self.display_error("Invalid smart home number.")
                except ValueError:
                    self.display_error("Please enter a valid number.")

            # List all devices in the network
            elif choice == "4":
                self.display_info("All Devices in Network:")
                device_count = 0
                for home in self.connected_network.smart_homes:
                    if home.smart_devices:
                        print(f"  {Fore.BLUE}■ Smart Home: {home.name}{Style.RESET_ALL}")
                        for device in home.smart_devices:
                            status = f"{Fore.GREEN}ON{Style.RESET_ALL}" if device.is_on else f"{Fore.RED}OFF{Style.RESET_ALL}"
                            print(f"    {Fore.YELLOW}►{Style.RESET_ALL} {device.name} ({device.device_type}) - {status}")
                            device_count += 1

                if device_count == 0:
                    print(f"  {Fore.YELLOW}No devices found in any smart home{Style.RESET_ALL}")

            # Disconnect from the network
            elif choice == "5":
                confirm = self.prompt("Are you sure you want to disconnect from the network? (yes/no)").strip().lower()
                if confirm == "yes":
                    self.logged_in_user.disconnect_from_network()
                    self.connected_network = None
                    self.display_success("Disconnected from network successfully!")
                else:
                    self.display_info("Disconnection cancelled.")

            # Back to main menu
            elif choice == "6":
                break

            # Invalid choice
            else:
                self.display_warning("Invalid choice. Please try again.")

    # Main loop for the main menus
    def loop(self):
        while True:
            if self.logged_in_user is None:
                x = self.logged_out()
            else:
                x = self.logged_in()
            if x:
                break
            time.sleep(1)

    # Load all scheduled operations
    def load_scheduals(self):
        try:
            SmartDevice.SmartDevice.scheduled_operations = self.scheduled_operations
            devices = []
            for i in self.networks:
                devices.append(i.list_smart_devices())
            for x in devices:
                for y in x:
                    if isinstance(y, SmartDevice.SmartDevice):
                        for z in self.scheduled_operations:
                            if z.device_serial_number == y.serial_number:
                                z.load(y)
            self.scheduled_operations = []
        except FileNotFoundError:
            self.display_error("No scheduled operations found. Please load the data file.")


if __name__ == "__main__":
    #change this to False if you want to load the data from the file
    #change this to True if you want to start with a fresh GUI
    first_start = False
    if first_start:
        gui = GUI()
        gui.add_network(Network.Network("1"))
        gui.add_network(Network.Network("2"))
    else:
        # Load the GUI from the saved data file
        with open("data.pkl", "rb") as f:
            gui = pickle.load(f)
        # Load the scheduled operations
        gui.load_scheduals()
        # Update the device count
        SmartDevice.SmartDevice._device_count = gui.device_count
        User.User._Users = gui.user_count
    # Start the program
    gui.loop()
    # Save the GUI state to a file
    gui.scheduled_operations = SmartDevice.SmartDevice.scheduled_operations
    gui.device_count = SmartDevice.SmartDevice.get_device_count()
    gui.user_count = User.User.get_user_count()
    with open("data.pkl", "wb") as f:
        pickle.dump(gui, f)
