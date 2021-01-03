import matplotlib.pyplot as plt
import numpy as np
import sys
# import ST7789 as ST7789
from PIL import Image


def ConfigurePlot(plot, title):
    plot.yaxis.set_tick_params(
        labelsize=2, width=0.25, length=1, pad=0.5)
    plot.xaxis.set_visible(False)
    plot.set_title(title, fontsize=3, pad=1)


# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

ax1.plot(x, y, linewidth=0.5)
ConfigurePlot(ax1, "Temperature")

ax2.plot(x, y**2, 'tab:orange', linewidth=0.5)
ConfigurePlot(ax2, "Humidity")

ax3.plot(x, -y, 'tab:green', linewidth=0.5)
ConfigurePlot(ax3, "Pressure")

ax4.plot(x, -y**2, 'tab:red', linewidth=0.5)
ConfigurePlot(ax4, "Quality")

# https://stackabuse.com/save-plot-as-image-with-matplotlib/
image_file = 'saved_chart.png'
fig.tight_layout(pad=2, h_pad=2, w_pad=3.5, rect=[0.035, -0.04, 1.02, 1])
fig.set_dpi(261.09)
fig.set_size_inches(0.9213, 0.9213)
plt.savefig(image_file)

img = Image.open(image_file)
img.show()

# disp = ST7789.ST7789(
#     port=0,
#     cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
#     dc=9,
#     backlight=19,               # 18 for back BG slot, 19 for front BG slot.
#     spi_speed_hz=80 * 1000 * 1000
# )

# WIDTH = disp.width
# HEIGHT = disp.height

# # Initialize display.
# disp.begin()

# # Load an image.
# print('Loading image: {}...'.format(image_file))
# image = Image.open(image_file)

# # Resize the image
# image = image.resize((WIDTH, HEIGHT))

# # Draw the image on the display hardware.
# print('Drawing image')

# disp.display(image)
