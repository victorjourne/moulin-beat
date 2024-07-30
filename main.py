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

n = 100  # Number of samples in series
period = 10    # Period of sampling (in milliseconds)
gain = 10      # Gain factor
sl_n = [0] * n  # Initialize sound level list with zeros
energy_n = [0] * n  # Initialize energy list with zeros
window_size = 10  # Window size for energy calculation
threshold = 1.1  # Threshold for peak detection
max_peaks = 10  # Maximum number of peak times to store
peak_times = []  # List to store the times of detected peaks
i, x = 0, 0  # Initialize index

running_sum = 0  # Running sum for energy calculation
print('yo')
while True:
    sleep(period / 1000.0)  # Sleep for the sampling period
    sl = microphone.sound_level() * gain  # Get sound level and apply gain
    i = (i + 1) % n  # Update index circularly

    # Update running sum for the sliding window energy calculation
    if i < window_size:
        running_sum += sl ** 2
    else:
        running_sum += sl ** 2 - sl_n[i - window_size] ** 2

    sl_n[i] = sl  # Store the sound level
    energy = running_sum / window_size  # Calculate average energy over the window
    energy_n[i] = energy  # Store the calculated energy

    # Calculate the average energy of all stored energies
    avg_energy = sum(energy_n) / n

    prev_index = (i - 1) % n
    prev_prev_index = (i - 2) % n
    if i > 1 and energy_n[i] > threshold * avg_energy and energy_n[prev_index] > energy_n[prev_prev_index] and energy_n[prev_index] > energy_n[i]:
        peak_times.append(running_time())  # Store the time of the detected peak in millisecond
        if len(peak_times) > max_peaks:
            peak_times.pop(0)  # Remove the oldest peak time to maintain the list size
        display.show(Image.HEART)
    else:
        display.clear()
    # Calculate tempo based on peak intervals
    if len(peak_times) > 1:
        # Calculate intervals between consecutive peaks
        intervals = [peak_times[j] - peak_times[j - 1] for j in range(1, len(peak_times))]
        
        # Calculate the average interval
        avg_interval = sum(intervals) / len(intervals)

        # Debugging output
        #print("Intervals (ms) : ",intervals)
        #print("Average interval (ms): ", avg_interval)
        
        # Calculate tempo in beats per minute (BPM)
        bpm = 60000 / avg_interval  # Convert from milliseconds to minutes
        
        print("Estimated tempo : ", bpm)
