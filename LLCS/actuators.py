
import bluerobotics_navigator as navigator
from bluerobotics_navigator import PwmChannel
import HLCS

if __name__ == "__main__":
    print("This script is not meant to be run directly")


class Motor:
    def __init__(self):
        self.pwm_freq = 54.28
        self.pwm_value_neutral = 365
        self.pwm_value_max_clockwise = 493 #437
        self.pwm_value_max_anticlockwise = 237

        self.pwm_channel = PwmChannel.Ch1

        navigator.set_pwm_freq_hz(self.pwm_freq)


    def actuation(self, input) -> None:

        pwm_value = int(HLCS.pid.lerp(input, -1, 1, self.pwm_value_max_anticlockwise, self.pwm_value_max_clockwise))

        navigator.set_pwm_channel_value(PwmChannel.Ch1, pwm_value)

        print(f"pwm_value: {pwm_value}")
        # print(f"input: {input} neutranInput: {neutranInput} forwardMaxInput: {forwardMaxInput} backwardMaxInput: {backwardMaxInput}")
        # if input > neutranInput:
        #     navigator.set_neopixel([[0, int((input - neutranInput) / (forwardMaxInput - neutranInput) * 128), 0]])
        # elif input == neutranInput:
        #     navigator.set_neopixel([[0, 0, 0]])
        # else:
        #     navigator.set_neopixel([[int((neutranInput - input) / (neutranInput - backwardMaxInput) * 128), 0, 0]])

    
    def start_up(self):

        navigator.set_pwm_channel_value(self.pwm_channel, self.pwm_value_neutral)
        navigator.set_pwm_enable(True)

    
    def shut_down(self):

        navigator.set_pwm_channel_value(self.pwm_channel, self.pwm_value_neutral)
        navigator.set_pwm_enable(False)
