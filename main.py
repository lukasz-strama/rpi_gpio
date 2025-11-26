import time
import sys
from rpi_toolkit import (
    gpio_init, gpio_cleanup, pin_mode, digital_write, 
    timer_set, timer_tick, millis, pwm_init, pwm_write, pwm_stop,
    SimpleTimer, OUTPUT, HIGH, LOW
)

def main():
    if gpio_init() != 0:
        print("Failed to initialize GPIO", file=sys.stderr)
        return 1

    led_pin = 21
    pwm_pin = 18

    print(f"Starting Python GPIO Blink on Pin {led_pin}...")
    print(f"Starting Python PWM on Pin {pwm_pin}...")

    pin_mode(led_pin, OUTPUT)

    if pwm_init(pwm_pin) != 0:
        print("Failed to init PWM", file=sys.stderr)

    blink_timer = SimpleTimer()
    sensor_timer = SimpleTimer()
    pwm_timer = SimpleTimer()

    timer_set(blink_timer, 500)
    timer_set(sensor_timer, 100)
    timer_set(pwm_timer, 1000)

    led_state = LOW
    pwm_duty = 0
    pwm_step = 25

    # Run for 5 seconds
    start_time = millis()
    while millis() - start_time < 5000:
        
        if timer_tick(blink_timer):
            led_state = not led_state
            digital_write(led_pin, HIGH if led_state else LOW)
            print(f"Blink! LED is {'HIGH' if led_state else 'LOW'}")

        if timer_tick(sensor_timer):
            # print("Checking sensors...") 
            pass

        if timer_tick(pwm_timer):
            pwm_duty += pwm_step
            if pwm_duty > 100:
                pwm_duty = 0
            pwm_write(pwm_pin, pwm_duty)

        # minimal sleep to prevent CPU hogging
        time.sleep(0.001)

    pwm_stop(pwm_pin)
    gpio_cleanup()
    print("Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
