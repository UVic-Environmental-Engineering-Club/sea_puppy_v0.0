
import HLCS
import LLCS
import sys
import time
import math
import threading
import queue

def input_listener(stop_queue):
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            stop_queue.put(True)
            break


def main():
    print("Hello World")
    llcs = LLCS.LLCS()
    hlcs = HLCS.HLCS()
    pid_kp = float(input("Enter the value of Kp: "))
    pid_ki = float(input("Enter the value of Ki: "))
    pid_kd = float(input("Enter the value of Kd: "))
    pid_controller = HLCS.pid.PIDController(kp = pid_kp, ki = pid_ki, kd = pid_kd, integral_limit = 1, output_limit = 1)

    llcs.calibrate()

    stop_queue = queue.Queue()
    input_thread = threading.Thread(target=input_listener, args=(stop_queue,))
    input_thread.start()

    running = True
    while running:
        if not stop_queue.empty():
            running = False

        pid_output = pid_controller.update(hlcs.target, llcs.get_pitch(), time.time())
        print(f"PID output: {pid_output}")

        # if pid_output >= 0:
        #     pwm_value = min(pwm_value_max_forward_clockwise, pwm_value_neutral + int((pwm_value_max_forward_clockwise - pwm_value_neutral) * (pid_output / math.pi)))
        # elif pid_output == 0:
        #     pwm_value = pwm_value_neutral
        # else:
        #     pwm_value = max(pwm_value_max_backword_anticlockwise, pwm_value_neutral + int((pwm_value_neutral - pwm_value_max_backword_anticlockwise) * (pid_output / math.pi)))

        llcs.read_and_print_angles()
        llcs.actuation(pid_output)
        #if (pwm_value + pwm_step >= pwm_value_max_forward_clockwise):
        #    pwm_toggle = False
        #elif (pwm_value - pwm_step <= pwm_value_max_backword_anticlockwise):
        #    pwm_toggle = True
        #if pwm_toggle:
        #    pwm_value += pwm_step
        #else:
        #    pwm_value -= pwm_step
        time.sleep(0.2)

    llcs.onShutdown()


if __name__ == "__main__":
    main()
