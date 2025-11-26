#define RPI_GPIO_IMPLEMENTATION
#include "rpi_gpio.h"
#define SIMPLE_TIMER_IMPLEMENTATION
#include "simple_timer.h"
#include <unistd.h>
#include <stdio.h>

int main() {
    if (gpio_init() != 0) {
        fprintf(stderr, "Failed to initialize GPIO\n");
        return 1;
    }

    int led_pin = 21;
    printf("Starting Non-Blocking GPIO Blink on Pin %d...\n", led_pin);
    
    pin_mode(led_pin, OUTPUT);

    simple_timer_t blink_timer;
    simple_timer_t sensor_timer;

    timer_set(&blink_timer, 500);
    timer_set(&sensor_timer, 100);

    int led_state = LOW;

    // Run for 5 seconds
    uint64_t start_time = millis();
    while (millis() - start_time < 5000) {
        
        if (timer_tick(&blink_timer)) {
            led_state = !led_state;
            digital_write(led_pin, led_state);
            printf("Blink! LED is %s\n", led_state ? "HIGH" : "LOW");
        }

        if (timer_tick(&sensor_timer)) {
            printf("Checking sensors...\n");
        }

        // minimal sleep to prevent CPU hogging
        usleep(1000); 
    }

    gpio_cleanup();
    printf("Done.\n");
    return 0;
}
