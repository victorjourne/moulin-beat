# Imports go at the top
from microbit import *
from math import *
from neopixel import NeoPixel
from maqueen import Maqueen

mq = Maqueen()

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
decay = 10 # decay of motor impulsion
sl_n = [0] * n  # Initialize sound level list with zeros
energy_n = [0] * n  # Initialize energy list with zeros
window_size = 10  # Window size for energy calculation
threshold = 1.2  # Threshold for peak detection
i, x = 0, 0  # Initialize index
i_pic = 0
running_sum = 0  # Running sum for energy calculation
motor_value = 0


# Signal avec les basses frequences
# https://en.wikipedia.org/wiki/Low-pass_filter
sl_low_freq = n * [0]
# Frequence de coupure en Hz, on filtre les frequence plus petite
fc_low = 3
alpha_low = 2 * pi * period * fc_low / (2 * pi * period * fc_low + 1000)
print(alpha_low)

# Signal avec les hautes frequences
# https://en.wikipedia.org/wiki/High-pass_filter
sl_high_freq = n * [0]
# Frequence de coupure en Hz, on filtre les frequence plus grande
fc_high = 100
alpha_high = 1000 / (2 * pi * period * fc_high + 1000)
print(alpha_high)
# If fc_high=fc_low
# then alpha_high = 1 - alpha_low and the computation is the same

while True:
    sleep(period / 1000.0)  # Sleep for the sampling period
    sl = microphone.sound_level() * gain  # Get sound level and apply gain
    i = (i + 1) % n  # Update index circularly
    prev_index = (i - 1) % n
    prev_prev_index = (i - 2) % n
    
    sl_n[i] = sl  # Store the sound level
    sl_low_freq[i] = alpha_low * sl_n[i] + (1 - alpha_low) * sl_low_freq[prev_index]
    sl_high_freq[i] = alpha_high * sl_high_freq[prev_index] + (1 - alpha_high) * (sl_n[i] - sl_n[prev_index])

    energy = 0
    for j in range(window_size):
        energy += sl_low_freq[(i - j) % n] ** 2  # Sum of squares of the last window_size samples
    energy /= window_size  # Average energy over the window
    energy_n[i] = energy  # Store the calculated energy

    # Calculate the average energy of all stored energies
    avg_energy = sum(energy_n) / n

    if i > 1 and energy_n[i] > threshold * avg_energy and energy_n[prev_index] > energy_n[prev_prev_index] and energy_n[prev_index] > energy_n[i]:
        display.show(Image.HEART)
        i_pic = i
        motor_value = int((energy_n[i] - threshold * avg_energy) * gain)
    # elif i > (i_pic + 10) % n:
    else:
        motor_value = int(motor_value // decay)
    # else:
    #     motor_value = 0

    mq.set_motor(0, motor_value)
    mq.set_motor(1, -motor_value)
    ledrgb(1, 0, motor_value, 0)
    ledrgb(2, 0, motor_value, 0)
