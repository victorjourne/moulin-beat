# Imports go at the top
from microbit import *
from math import *
from neopixel import NeoPixel

# from maqueen import Maqueen

# mq = Maqueen()


x, i = 0, 0
max_level = 50
# image = 5 * ['00000']
# while True:
#     x = (x + 1) % 4
#     sl = microphone.sound_level()
#     y = min(4, int((sl / max_level ) * 4))
#     row = "{num:0>5}".format(num="9" * y)
#     print(row)
#     image[x] = row
#     display.show(Image(":".join(image)))

# Put it in maqueen
def ledrgb(n,r,g,b):
    n=min(max(n,0),3)
    r=min(max(r,0),255)
    g=min(max(g,0),255)
    b=min(max(b,0),255)
    np=NeoPixel(pin15,4)
    np[floor(n)]=(floor(r),floor(g),floor(b))
    np.show()

def mean(n):
    sum = 0
    for i in n:
        sum += i
    return int(sum / len(n))
    
    n = 1000  # Number of samples in series
    period = 10    # Period of sampling (in milliseconds)
    gain = 10      # Gain factor
    sl_n = [0] * n  # Initialize sound level list with zeros
    energy_n = [0] * n  # Initialize energy list with zeros
    window_size = 10  # Window size for energy calculation
    threshold = 1.2  # Threshold for peak detection

    i, x = 0, 0  # Initialize index

    while True:
        time.sleep(period / 1000.0)  # Sleep for the sampling period
        # Write new line
        x = (x + 1) % 5
        sl = microphone.sound_level() * gain  # Get sound level and apply gain
        i = (i + 1) % n  # Update index circularly
        sl_n[i] = sl  # Store the sound level

        # Calculate the energy of the signal in the current window
        energy = 0
        for j in range(window_size):
            energy += sl_n[(i - j) % n] ** 2  # Sum of squares of the last window_size samples
        energy /= window_size  # Average energy over the window
        energy_n[i] = energy  # Store the calculated energy

        # Calculate the average energy of all stored energies
        avg_energy = sum(energy_n) / n

        # Detect peak only at the most recent index
        if energy_n[i] > threshold * avg_energy and energy_n[i] > energy_n[i - 1] and energy_n[i] > energy_n[(i + 1) % n]:
            print(f"Detected peak at index: {i}")
            display.show(Image.HEART)
        # Perform other actions based on detected peaks
        # ...