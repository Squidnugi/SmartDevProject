import time as time_module
import threading
import SmartDevice


def test():
    smart_device = SmartDevice.SmartLight("TestLight", brightness=75)
    smart_device.delay_operation("turn_on", 2)  # Turn on after 2 seconds
    smart_device.schedule_operation("turn_off", "11:22")  # Turn off at 12:43
    smart_device.delay_operation("set_brightness", 1, 30)  # Set brightness to 30 after 1 second


    while True:
        thing = input(">>")
        if thing == "exit":
            break


if __name__ == "__main__":
    test()