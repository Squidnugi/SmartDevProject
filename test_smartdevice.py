import pytest
from SmartDevice import SmartDevice, SmartLight



class DummyNetwork:
    def __init__(self, ip_address="192.168.1.1"):
        self.ip_address = ip_address

@pytest.fixture
def smart_light():
    return SmartLight("TestLight", brightness=75)


def test_turn_on_off(smart_light):
    smart_light.turn_on()
    assert smart_light.is_on
    smart_light.turn_off()
    assert not smart_light.is_on


def test_set_energy_consumption(smart_light):
    smart_light.set_energy_consumption(5.5)
    assert smart_light.energy_consumption == 5.5


def test_connect_disconnect(smart_light):
    network = DummyNetwork()
    smart_light.connect(network)
    assert smart_light.network == network
    smart_light.disconnect()
    assert smart_light.network is None


def test_device_count():
    count_before = SmartDevice.get_device_count()
    d = SmartLight("AnotherLight")
    count_after = SmartDevice.get_device_count()
    assert count_after == count_before + 1

def test_schedule_operation(smart_light):
    smart_light.turn_on()
    smart_light.schedule_operation("turn_off", 60)
    assert not smart_light.is_on  # Assuming the operation completes immediately in the test environment

