//
//  HCSR04.c
//
//  http://elinux.org/RPi_Low-level_peripherals#C
//  http://rasathus.blogspot.co.uk/2012/09/ultra-cheap-ultrasonics-with-hy-srf05_27.html
//  Created by Marko Sahlman on 19/05/15.

#include <stdio.h>
#include <Python.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define IN  0
#define OUT 1

#define LOW  0
#define HIGH 1

#define TIMEOUT 999 /* any value other than LOW or HIGH */


static int
GPIOExport(int pin)
{
#define BUFFER_MAX 3
    char buffer[BUFFER_MAX];
    ssize_t bytes_written;
    int fd;
    
    fd = open("/sys/class/gpio/export", O_WRONLY);
    if (-1 == fd) {
        fprintf(stderr, "Failed to open export for writing!\n");
        return(-1);
    }
    
    bytes_written = snprintf(buffer, BUFFER_MAX, "%d", pin);
    write(fd, buffer, bytes_written);
    close(fd);
    return(0);
}


static int
GPIOUnexport(int pin)
{
    char buffer[BUFFER_MAX];
    ssize_t bytes_written;
    int fd;
    
    fd = open("/sys/class/gpio/unexport", O_WRONLY);
    if (-1 == fd) {
        fprintf(stderr, "Failed to open unexport for writing!\n");
        return(-1);
    }
    
    bytes_written = snprintf(buffer, BUFFER_MAX, "%d", pin);
    write(fd, buffer, bytes_written);
    close(fd);
    return(0);
}


static int
GPIODirection(int pin, int dir)
{
    static const char s_directions_str[]  = "in\0out";
    
#define DIRECTION_MAX 35
    char path[DIRECTION_MAX];
    int fd;
    
    snprintf(path, DIRECTION_MAX, "/sys/class/gpio/gpio%d/direction", pin);
    fd = open(path, O_WRONLY);
    if (-1 == fd) {
        fprintf(stderr, "Failed to open gpio direction for writing!\n");
        return(-1);
    }
    
    if (-1 == write(fd, &s_directions_str[IN == dir ? 0 : 3], IN == dir ? 2 : 3)) {
        fprintf(stderr, "Failed to set direction!\n");
        return(-1);
    }
    
    close(fd);
    return(0);
}

static int
GPIORead(int pin)
{
#define VALUE_MAX 30
    char path[VALUE_MAX];
    char value_str[3];
    int fd;
    
    snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", pin);
    fd = open(path, O_RDONLY);
    if (-1 == fd) {
        fprintf(stderr, "Failed to open gpio value for reading!\n");
        return(-1);
    }
    
    if (-1 == read(fd, value_str, 3)) {
        fprintf(stderr, "Failed to read value!\n");
        return(-1);
    }
    
    close(fd);
    
    return(atoi(value_str));
}

static int
GPIOWrite(int pin, int value)
{
    static const char s_values_str[] = "01";
    
    char path[VALUE_MAX];
    int fd;
    
    snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", pin);
    fd = open(path, O_WRONLY);
    if (-1 == fd) {
        fprintf(stderr, "Failed to open gpio value for writing!\n");
        return(-1);
    }
    
    if (1 != write(fd, &s_values_str[LOW == value ? 0 : 1], 1)) {
        fprintf(stderr, "Failed to write value!\n");
        return(-1);
    }
    
    close(fd);
    return(0);
}

int waitforpin(int pin, int level, int timeout)
{
    struct timeval now, start;
    int done;
    long micros;
    gettimeofday(&start, NULL);
    micros = 0;
    done=0;
    while (!done)
    {
        gettimeofday(&now, NULL);
        if (now.tv_sec > start.tv_sec) micros = 1000000L; else micros = 0;
        micros = micros + (now.tv_usec - start.tv_usec);
        if (micros > timeout) done=1;
        if (GPIORead(pin) == level) done = 1;
    }
    return micros;
}


static PyObject*
readvalue(PyObject* self, PyObject* args)
{
    const int gpio_trigger_pin, gpio_echo_pin;
    
    if (!PyArg_ParseTuple(args, "ii", &gpio_trigger_pin, &gpio_echo_pin))
        return NULL;
    

    /*
     * Enable GPIO pins
     */
    if (-1 == GPIOExport(gpio_trigger_pin) || -1 == GPIOExport(gpio_echo_pin))
        Py_RETURN_NONE; // Raise error here
    
    /*
     * Set directions
     */
    if (-1 == GPIODirection(gpio_trigger_pin, OUT) || -1 == GPIODirection(gpio_echo_pin, IN))
        Py_RETURN_NONE; // Raise error here
    
    GPIOWrite(gpio_trigger_pin, LOW);

    // Waiting sensor to settle for 2 seconds (2 seconds in microseconds)
    usleep(2000000);
    
    // Send 10uS pulse into trigger pin
    GPIOWrite(gpio_trigger_pin, HIGH);
    waitforpin(gpio_echo_pin, TIMEOUT, 10); /* wait 10 microseconds */
    GPIOWrite(gpio_trigger_pin, LOW);
    waitforpin(gpio_echo_pin, HIGH, 5000); /* 5 ms timeout */
    
    int pulsewidth = -1;
    
    if (GPIORead(gpio_echo_pin) == HIGH) {

        pulsewidth = waitforpin(gpio_echo_pin, LOW, 60000L); /* 60 ms timeout */
        if (GPIORead(gpio_echo_pin) == LOW)
        {
            /* valid reading code */
            printf("echo at %d micros\n", pulsewidth / 2);
        }
        else
        {
            /* no object detected code */
            printf("echo timed out\n");
        }
    
    } else {
        printf("Sensor failed");
    }

    
    if (-1 == GPIOUnexport(gpio_trigger_pin) || -1 == GPIOUnexport(gpio_echo_pin))
        Py_RETURN_NONE; // Raise error here

    
    
    
    
    return Py_BuildValue("i", pulsewidth);
}

static PyMethodDef HCSR04Methods[] =
{
    {"readvalue", readvalue, METH_VARARGS, "Read value"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initHCSR04(void)
{
    (void) Py_InitModule("HCSR04", HCSR04Methods);
}