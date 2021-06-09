import marker
import pid
import numpy as np
import matplotlib.pyplot as plt
from control import tf, feedback, step_response

# model
# input u, force
# output v, velocity
# mv. + bv = u
# msV + bV = U
# V/U = 1 / (ms + b)

# controller
# pid = Kp + Ki/s + Kd*s

TIME_STEP = 0.1
END_TIME = 100
TIME = np.arange(TIME_STEP, END_TIME+TIME_STEP, TIME_STEP)

mass = 1000  # kg
b = 50  # damping constant
REF = 10  # vel m/s

KP = 800
KI = 40
KD = 100
s = tf('s')
plant = 1 / (mass*s + b)
controller = KP + KI/s + KD*s
h = feedback(controller*plant, 1)

t, y = step_response(REF*h)
r = REF * np.ones(len(t))
plt.figure(1)
plt.plot(t, y)
plt.plot(t, r)
plt.show()
