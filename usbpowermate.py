from __future__ import print_function
from ctypes import c_byte
import threading
from collections import defaultdict
from pywinusb.hid import HidDeviceFilter

def to_signed(unsigned):
    return c_byte(unsigned).value
  
class Powermate():
    VENDOR = 0x077d
    PRODUCT = 0x0410
    MOVE_LEFT = -1
    MOVE_NONE = 0
    MOVE_RIGHT = 1
    BUTTON_DOWN = 1
    BUTTON_UP = 0
    
    def __init__(self, device):
        self.__device = device
        self.__device.set_raw_data_handler(lambda raw_data: self.__internal_listener(raw_data))
        self.__events = defaultdict(set)
        self._rotation_lock = threading.Lock()
        self._pressed_lock = threading.Lock()
        self.button = 0
        self._rotation = 0
        self._pressed = True
        
    @classmethod
    def find(cls):
        return [Powermate(d) for d in HidDeviceFilter(vendor_id=cls.VENDOR, product_id=cls.PRODUCT).get_devices()]
  
    def __internal_listener(self, raw_data):
        """
        [0, button_status, raw_move, 0, brightness, pulse_status, pulse_value]
        """
        _, button_status, raw_move, _, brightness, pulse_status, pulse_value = raw_data
        move = to_signed(raw_move)
        if button_status == 1 and self.button == 0:
            self.set_pressed()
        self.button = button_status
        self.rotate(move)

    def open(self):
        if not self.__device.is_opened():
            self.__device.open()

    def close(self):
        if self.__device.is_opened():
            self.__device.close()
        
    def rotate(self, val):
        self._rotation_lock.acquire()
        self._rotation += val
        self._rotation_lock.release()
    
    def get_rotation(self):
        self._rotation_lock.acquire()
        val, self._rotation = self._rotation, 0
        self._rotation_lock.release()
        return val
    
    def set_pressed(self):
        self._pressed_lock.acquire()
        self._pressed = True
        self._pressed_lock.release()
        
    def get_pressed(self):
        self._pressed_lock.acquire()
        val, self._pressed = self._pressed, False
        self._pressed_lock.release()
        return val