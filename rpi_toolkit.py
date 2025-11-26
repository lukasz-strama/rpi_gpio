import ctypes
import os
import sys

# Load the shared library
# Lib assume libtoolkit.so is in the same directory as this script
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libtoolkit.so")
if not os.path.exists(lib_path):
    raise FileNotFoundError(f"Could not find {lib_path}. Did you run 'make'?")

_lib = ctypes.CDLL(lib_path)

# Constants
INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1

# Type Definitions
class SimpleTimer(ctypes.Structure):
    _fields_ = [
        ("next_expiry", ctypes.c_uint64),
        ("interval", ctypes.c_uint64)
    ]

# Function Signatures

# int gpio_init(void);
_lib.gpio_init.argtypes = []
_lib.gpio_init.restype = ctypes.c_int

# void gpio_cleanup(void);
_lib.gpio_cleanup.argtypes = []
_lib.gpio_cleanup.restype = None

# void pin_mode(int pin, int mode);
_lib.pin_mode.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.pin_mode.restype = None

# void digital_write(int pin, int value);
_lib.digital_write.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.digital_write.restype = None

# int digital_read(int pin);
_lib.digital_read.argtypes = [ctypes.c_int]
_lib.digital_read.restype = ctypes.c_int

# void timer_set(simple_timer_t* t, uint64_t interval_ms);
_lib.timer_set.argtypes = [ctypes.POINTER(SimpleTimer), ctypes.c_uint64]
_lib.timer_set.restype = None

# bool timer_expired(simple_timer_t* t);
_lib.timer_expired.argtypes = [ctypes.POINTER(SimpleTimer)]
_lib.timer_expired.restype = ctypes.c_bool

# bool timer_tick(simple_timer_t* t);
_lib.timer_tick.argtypes = [ctypes.POINTER(SimpleTimer)]
_lib.timer_tick.restype = ctypes.c_bool

# uint64_t millis(void);
_lib.millis.argtypes = []
_lib.millis.restype = ctypes.c_uint64

# uint64_t micros(void);
_lib.micros.argtypes = []
_lib.micros.restype = ctypes.c_uint64

# void delay_us(uint64_t us);
_lib.delay_us.argtypes = [ctypes.c_uint64]
_lib.delay_us.restype = None

# int pwm_init(int pin);
_lib.pwm_init.argtypes = [ctypes.c_int]
_lib.pwm_init.restype = ctypes.c_int

# void pwm_write(int pin, int duty);
_lib.pwm_write.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.pwm_write.restype = None

# void pwm_stop(int pin);
_lib.pwm_stop.argtypes = [ctypes.c_int]
_lib.pwm_stop.restype = None


# Python Wrapper Functions

def gpio_init():
    return _lib.gpio_init()

def gpio_cleanup():
    _lib.gpio_cleanup()

def pin_mode(pin, mode):
    _lib.pin_mode(pin, mode)

def digital_write(pin, value):
    _lib.digital_write(pin, value)

def digital_read(pin):
    return _lib.digital_read(pin)

def timer_set(timer, interval_ms):
    _lib.timer_set(ctypes.byref(timer), interval_ms)

def timer_expired(timer):
    return _lib.timer_expired(ctypes.byref(timer))

def timer_tick(timer):
    return _lib.timer_tick(ctypes.byref(timer))

def millis():
    return _lib.millis()

def micros():
    return _lib.micros()

def delay_us(us):
    _lib.delay_us(us)

def pwm_init(pin):
    return _lib.pwm_init(pin)

def pwm_write(pin, duty):
    _lib.pwm_write(pin, duty)

def pwm_stop(pin):
    _lib.pwm_stop(pin)
