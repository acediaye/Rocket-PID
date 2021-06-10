import numpy as np


class PID(object):
    def __init__(self, KP, KI, KD):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.error = 0
        self.prev_error = 0
        self.prev_time = 0
        self.proportional_error = 0
        self.integral_error = 0
        self.derivative_error = 0
        self.u_output = 0
        self.count = 0
        self.max_output = 100
        self.min_output = 0
        self.max_integral = 0
        self.min_integral = 0

    def controller(self, reference: float, measured_value: float, time: float):
        self.error = reference - measured_value
        self.proportional_error = self.error
        self.integral_error += self.error * (time - self.prev_time)
        # # capping integral
        # if self.integral_error > MAX_INTEGRAL:
        #     self.integral_error = MAX_INTEGRAL
        # elif self.integral_error < -MAX_INTEGRAL:
        #     self.integral_error = -MAX_INTEGRAL
        self.derivative_error = ((self.error - self.prev_error)
                                 / (time - self.prev_time))
        self.u_output = (self.kp * self.proportional_error
                         + self.ki * self.integral_error
                         + self.kd * self.derivative_error)
        self.prev_error = self.error
        self.prev_time = time
        # saturation
        if self.u_output > self.max_output:
            self.u_output = self.max_output
        elif self.u_output < self.min_output:
            self.u_output = self.min_output
        print(f'u: {self.u_output}, r: {reference}, '
              f'y: {measured_value}, e: {self.error}')
        self.count += 1
        return self.u_output

    def get_error(self):
        return self.error

    def get_kpe(self):
        return self.kp * self.proportional_error

    def get_kie(self):
        return self.ki * self.integral_error

    def get_kde(self):
        return self.kd * self.derivative_error

    def ziegler_tune(self, ku: float, tu: float):
        self.kp = 0.6 * ku
        self.ki = 1.2 * ku / tu
        self.kd = 0.075 * ku * tu

    def set_output_saturation(self, min, max):
        self.min_output = min
        self.max_output = max

    def set_integral_saturation(self, min, max):
        self.min_integral = min
        self.max_integral = max
