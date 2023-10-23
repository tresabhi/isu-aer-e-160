import numpy as np
from matplotlib import pyplot as pl
import pint

ur = pint.UnitRegistry()

arrow_length = 500 * ur.km
arrow_width= 300 * ur.km

rocket_empty_mass = 29500 * ur.kg
rocket_payload_mass = 1000 * ur.kg
rocket_fuel_mass = 480000 * ur.kg
rocket_mass = rocket_empty_mass + rocket_payload_mass + rocket_fuel_mass
rocket_tsfc = 3.5e-3 * ur.s / ur.m
rocket_full_thrust = 7600000 * ur.N

gravitational_constant = 6.674e-11 * ur.m ** 3 / (ur.kg * ur.s ** 2)

earth_mass = 5.98e24 * ur.kg
earth_diameter = 12700000 * ur.m
earth_equator_vel = 460 * ur.m / ur.s

position = np.array((0.0, earth_diameter.magnitude / 2.0)) * ur.m
velocity = np.array((0.0, 0.0)) * ur.m / ur.s

T_angle = 60.0 * ur.degree
T_direction = np.array((np.cos(T_angle.to(ur.rad).magnitude), np.sin(T_angle.to(ur.rad).magnitude)))

figure = plt.figure()
arrowplt = plt.arrow(
    position[0].magnitude,
    position[1].magnitude,
    T_direction[0] * arrow_length.to(ur.m).magnitude,
    T_direction[0] * arrow_length.to(ur.m).magnitude,
    width = arrow_width.to(ur.m).magnitude
)
earth = plt.Circle((0, 0), float(earth_diameter.magnitude / 2.0), color = 'g')

plt.ion()
plt.axis((-1e6, 1e6, 6e6, 7e6))
plt.grid(True)

figure.gca().add_artist(earth)
figure.gca().add_artist(arrowplt)