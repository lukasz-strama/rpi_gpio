/*
 * simple_timer.h - Single-header C library for non-blocking timing
 *
 * Usage:
 *   #define SIMPLE_TIMER_IMPLEMENTATION
 *   #include "simple_timer.h"
 *
 *   ...
 *   simple_timer_t t;
 *   timer_set(&t, 1000);
 *   if (timer_expired(&t)) { ... }
 *   ...
 */

#ifndef SIMPLE_TIMER_H
#define SIMPLE_TIMER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint64_t next_expiry;
    uint64_t interval;
} simple_timer_t;

// API Declarations
void timer_set(simple_timer_t* t, uint64_t interval_ms);
bool timer_expired(simple_timer_t* t);
bool timer_tick(simple_timer_t* t);
uint64_t millis(void);

#ifdef __cplusplus
}
#endif

#endif // SIMPLE_TIMER_H

#ifdef SIMPLE_TIMER_IMPLEMENTATION

#include <time.h>

uint64_t millis(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)(ts.tv_sec * 1000) + (uint64_t)(ts.tv_nsec / 1000000);
}

void timer_set(simple_timer_t* t, uint64_t interval_ms) {
    t->interval = interval_ms;
    t->next_expiry = millis() + interval_ms;
}

bool timer_expired(simple_timer_t* t) {
    uint64_t now = millis();
    if (now >= t->next_expiry) {
        return true;
    }
    return false;
}

bool timer_tick(simple_timer_t* t) {
    uint64_t now = millis();
    if (now >= t->next_expiry) {
        t->next_expiry += t->interval;
        return true;
    }
    return false;
}

#endif // SIMPLE_TIMER_IMPLEMENTATION
