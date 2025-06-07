import time as time_module
import threading
import SmartDevice
import pickle
from main import GUI

class MyData:
    def __init__(self, x):
        self.x = x

obj = MyData(10)

def test():
    smart_device = SmartDevice.SmartLight("TestLight", brightness=75)
    smart_device.delay_operation("turn_on", 2)  # Turn on after 2 seconds
    smart_device.schedule_operation("turn_off", "11:22")  # Turn off at 12:43
    smart_device.delay_operation("set_brightness", 1, 30)  # Set brightness to 30 after 1 second
    smart_device.schedule_operation("set_brightness", "17:20", 30)


    while True:
        thing = input(">>")
        if thing == "exit":
            break

def test2():
    smart_device = SmartDevice.SmartLight("TestLight", brightness=75)
    #smart_device2 = SmartDevice.SmartLight("TestLight2", brightness=75)
    saved_operation = SmartDevice.scheduled_operation(smart_device.serial_number, "toggle", "23:16", False)
    #saved_operation2 = SmartDevice.scheduled_operation(smart_device2.serial_number, "toggle", "22:22", False)
    #saved_operation3 = SmartDevice.scheduled_operation(smart_device2.serial_number, "set_brightness", "22:22", False, 50)
    #device_list = []
    #saved_operations = []
    #saved_operations.append(saved_operation)
    #saved_operations.append(saved_operation2)
    #saved_operations.append(saved_operation3)
    #device_list.append(smart_device)
    #device_list.append(smart_device2)
    #for x in saved_operations:
        #for i in device_list:
            #if i.serial_number == x.device_serial_number:
                #x.load(i)
    saved_operation.load(smart_device)

    while True:
        thing = input(">>")
        if thing == "exit":
            break

if __name__ == "__main__":
    with open("data.pkl", "rb") as f:
        gui = pickle.load(f)
    print(SmartDevice.SmartDevice.get_scheduled_operations())