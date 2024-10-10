
import sys
import time
import math

import bluerobotics_navigator as navigator

import LLCS



int_pitch = 0.0
int_roll = 0.0
int_yaw = 0.0
prev_time = 0.0


def testing_loop(print_info = False):
    global int_pitch
    global int_roll
    global int_yaw
    global prev_time

    next_time = time.time_ns()
    time_delta = (next_time - prev_time) / 1_000_000_000

    (pitch, roll, yaw) = LLCS.sensors.get_pitch_roll_yaw()
    ang_vel = navigator.read_gyro()

    if math.isnan(ang_vel.x) or math.isnan(ang_vel.y) or math.isnan(ang_vel.z) or math.isnan(pitch) or math.isnan(roll) or math.isnan(yaw):
        return

    int_pitch += ang_vel.y * time_delta
    int_roll += ang_vel.x * time_delta
    int_yaw += -ang_vel.z * time_delta

    if not print_info:
        return

    pitch_error = pitch - int_pitch
    roll_error = roll - int_roll
    yaw_error = yaw - int_yaw

    prev_time = next_time

    
    print(f"Delta: {time_delta:1.7f}, Error: ({pitch_error:1.5f}, {roll_error:1.5f}), Integrated: ({int_pitch:1.5f}, {int_roll:1.5f}), Actual: ({pitch:1.5f}, {roll:1.5f})")




def main():
    global int_pitch
    global int_roll
    global int_yaw
    global prev_time

    navigator.init()

    (int_pitch, int_roll, int_yaw) = LLCS.sensors.get_pitch_roll_yaw()
    
    prev_time = time.time_ns()


    try:
        i = 0
        while True:
            testing_loop(i % 100 == 0)
    finally:
        print("Done")



if __name__ == "__main__":
    main()
