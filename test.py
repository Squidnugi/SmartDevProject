import time as time_module
import threading

def test():
    delay = 5  # seconds
    def delayed_operation():
        time_module.sleep(delay)
        try:
            print("\nSmart light turned on after delay.")
        except Exception as e:
            print(f"Error during delayed operation: {e}")


    threading.Thread(target=delayed_operation).start()
    print("before thread?")
    val = input("Press Enter to continue...")
    print(val)

def test2():
    print("This is a test function that runs after the main thread completes.")
    # You can add more functionality here as needed.
    # For example, you could check the status of devices or perform cleanup tasks.
    return None
    print("This is a test function that runs before the main thread starts.")
if __name__ == "__main__":
    test2()