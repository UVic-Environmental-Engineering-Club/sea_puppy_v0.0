
import HLCS
import LLCS
import sys
import time
import math
import threading

running = True

hlcs = HLCS.HLCS()
llcs = LLCS.LLCS()
pid_controller = HLCS.pid.PIDController()


def control_loop():
    global hlcs
    global llcs
    global running
    global pid_controller

    while running:
        num_loops = 100
        ave_pid_output = 0
        ave_current_motor_input = 0
        ave_target_motor_input = 0

        pid_output = pid_controller.update(hlcs.target, llcs.get_pitch(), time.time())

        #for _ in range(num_loops):
        #    ave_pid_output += pid_output
        #    ave_current_motor_input += llcs.current_motor_input
        #    ave_target_motor_input += llcs.target_motor_input

        llcs.update(- pid_output)

        # print(f"ave pid output: {ave_pid_output / num_loops}")
        # print(f"ave current motor input: {ave_current_motor_input / num_loops}")
        # print(f"ave target motor input: {ave_target_motor_input / num_loops}")
        llcs.read_and_print_angles()



def main():
    global hlcs
    global llcs
    global pid_controller
    hlcsTarget = 0
    hlcsTarget = float(input("Enter target angle in degrees: ")) * math.pi / 180
    while hlcsTarget < 0 or hlcsTarget > 180:
        hlcsTarget = float(input("Enter target angle in degrees: ")) * math.pi / 180
        if hlcsTarget < 0 or hlcsTarget > 180:
            print("Invalid angle. Please enter an angle between 0 and 180 degrees.")

    hlcs.target = hlcsTarget

    pid_kp = 1
    pid_ki = 0.1
    pid_kd = 0
    pid_controller = HLCS.pid.PIDController(kp = pid_kp, ki = pid_ki, kd = pid_kd, integral_limit = 1, output_limit = 1)

    llcs.calibrate()

    try:
        control_loop()
    finally:
        llcs.onShutdown()


if __name__ == "__main__":
    main()
