#!/usr/bin/env python

import time
from array import *
import sys
import matplotlib.pyplot as plt
import numpy as np
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from sgp30 import SGP30
import ST7789 as ST7789
from PIL import Image

print("""Read temperature, pressure, humidity, and C02""")

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
sgp30 = SGP30()
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)
image_file = 'saved_chart.png'
WIDTH = disp.width
HEIGHT = disp.height

print("Sensor warming up, please wait...")
def crude_progress_bar():
    sys.stdout.write('.')
    sys.stdout.flush()

def ConfigurePlot(plot, title):
    plot.yaxis.set_tick_params(
        labelsize=2, width=0.25, length=1, pad=0.5)
    plot.xaxis.set_visible(False)
    plot.set_title(title, fontsize=3, pad=1)

sgp30.start_measurement(crude_progress_bar)
disp.begin()

temperatures = []
pressures = []
humidities = []
qualities = []
timestamps = []

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    quality = sgp30.get_air_quality()
    timestamp=time.mktime(time.localtime())
    
    print('{:05.2f}*C {:05.2f}hPa {:05.2f}% {:05.2f}ppm '.format(temperature, pressure, humidity, quality.equivalent_co2))
    
    if len(timestamps) > 100:
        temperatures.pop(0)
        pressures.pop(0)
        humidities.pop(0)
        qualities.pop(0)
        timestamps.pop(0)

    temperatures.append(round(temperature, 2))
    pressures.append(round(pressure, 2))
    humidities.append(round(humidity, 2))
    qualities.append(round(quality.equivalent_co2, 2))
    timestamps.append(timestamp)

    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    
    ConfigurePlot(ax1, "Temperature")
    ConfigurePlot(ax2, "Humidity")
    ConfigurePlot(ax3, "Pressure")
    ConfigurePlot(ax4, "Quality")
    
    ax1.plot(timestamps, temperatures, linewidth=0.5)
    ax2.plot(timestamps, humidities, 'tab:orange', linewidth=0.5)
    ax3.plot(timestamps, pressures, 'tab:green', linewidth=0.5)
    ax4.plot(timestamps, qualities, 'tab:red', linewidth=0.5)

    #fig.tight_layout(pad=2, h_pad=2, w_pad=3.5, rect=[0.035, -0.04, 1.02, 1])
    fig.set_dpi(261.09)
    fig.set_size_inches(0.9213, 0.9213)

    plt.savefig(image_file)
    image = Image.open(image_file)
    image = image.resize((WIDTH, HEIGHT))
    disp.display(image)
    time.sleep(6)
