from colorama import Fore, Style
import SmartDevice
import time
from abc import ABC, abstractmethod
import Network
import User

"""Each device will be attached to 1 network
devices can be under a hub
each smarthome is connected to 1 network
a user is not set by a network but can only be in 1 at a time
users can see their other devices in other networks not currently connected to
users are not directly connected to smartdevices, the creation of a smarthome is required first
there can be multiple smarthomes in a network
users connected to a network can see all the smarthomes in that network"""




def logged_out(network):
    print(Fore.CYAN + "Welcome to the Smart Home System!" + Style.RESET_ALL)
    print("1. Create a new user")
    print("2. log in")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter a username: ")
        user = next((user for user in users if user.username == username), None)
        if user:
            print(Fore.RED + f"Username {username} already exists" + Style.RESET_ALL)
            return None
        try:
            user = User.User(username)
            user.connect_to_network(network)
            users.append(user)
            print(Fore.GREEN + f"User {username} created successfully!" + Style.RESET_ALL)
            return user
        except ValueError as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            return None
    elif choice == "2":
        username = input("Enter your username: ")
        user = next((user for user in users if user.username == username), None)
        if user:
            print(Fore.GREEN + f"Welcome back, {username}!" + Style.RESET_ALL)
            return user
        else:
            print(Fore.RED + "User not found. Please create a new user." + Style.RESET_ALL)
            return None
    elif choice == "3":
        print(Fore.RED + "Exiting the system." + Style.RESET_ALL)
        exit()
    else:
        print(Fore.YELLOW + "Invalid choice. Please try again." + Style.RESET_ALL)
        return None


def logged_in(user, network):
    print(Fore.CYAN + "Welcome to the Smart Home System!" + Style.RESET_ALL)
    print("1. Create a new smart home")
    print("2. List smart homes")
    print("3. Connect to a smart home")
    print("4. Disconnect from a smart home")
    print("5. List devices in smart home")
    print("6. Create a new device")
    print("7. List devices in network")
    print("8. List devices in all smart homes")
    print("9. Select a device")
    print("10. Log out")
    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Enter a name for your smart home: ")
        smart_home = User.SmartHome(user.network, name)
        network.add_smart_home(smart_home)
        print(Fore.GREEN + f"Smart home {name} created successfully!" + Style.RESET_ALL)
        return user
    elif choice == "5":
        if not network.smart_homes:
            print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
            return user
        smart_home_name = input("Enter the name of the smart home: ")
        smart_home = next((home for home in network.smart_homes if home.name == smart_home_name), None)
        if smart_home:
            print(Fore.GREEN + f"Devices in {smart_home_name}:" + Style.RESET_ALL)
            for device in smart_home.smart_devices:
                print(device)
        else:
            print(Fore.RED + "Smart home not found." + Style.RESET_ALL)
    elif choice == "6":
        if not network.smart_homes:
            print(Fore.RED + "No smart homes found. Please create a smart home first." + Style.RESET_ALL)
            return user
        name = input("Enter a name for your device: ")
        print("List of Device Types:")
        print("1. Light")
        print("2. Thermostat")
        print("3. Camera")
        print("4. Lock")
        print("5. Speaker")
        print("6. Doorbell")
        print("7. Door")
        print("8. Appliance")
        print("9. None")
        device_type_choice = input("Enter the number of the device type: ")
        device_types = {
            "1": "Light",
            "2": "Thermostat",
            "3": "Camera",
            "4": "Lock",
            "5": "Speaker",
            "6": "Doorbell",
            "7": "Door",
            "8": "Appliance",
            "9": "None"
        }
        device_type = device_types.get(device_type_choice)
        if device_type == "None":
            device_type = input("Enter the type of device: ")
        smart_home_name = input("Enter the name of the smart home to add the device to: ")
        smart_home = next((home for home in network.smart_homes if home.name == smart_home_name), None)
        if smart_home:
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
                device = SmartDevice.SmartAppliance(name)
            else:
                device = SmartDevice.SmartDevice(name, device_type)
            smart_home.add_smart_device(device)
            print(Fore.GREEN + f"Device {name} created successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Smart home not found." + Style.RESET_ALL)
    elif choice == "10":
        print(Fore.RED + f"Logging out {user.username}..." + Style.RESET_ALL)
        user.disconnect_from_network()
        return None
    return user


if __name__ == "__main__":
    users = []
    logged_in_user = None
    network = Network.Network("19")
    while True:
        if logged_in_user is None:
            logged_in_user = logged_out(network)
        else:
            check = logged_in(logged_in_user, network)
            if check is None:
                logged_in_user = None
            else:
                logged_in_user = check


