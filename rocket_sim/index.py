import time
import numpy as np
from matplotlib import pyplot as plt
import pint

ur = pint.UnitRegistry()

arrow_length = 50 * ur.km
arrow_width= 30 * ur.km
simulation_time = 3600 * ur.s

rocket_empty_mass = 29500 * ur.kg
rocket_payload_mass = 1000 * ur.kg
rocket_fuel_mass = 480000 * ur.kg
rocket_mass = rocket_empty_mass + rocket_payload_mass + rocket_fuel_mass
rocket_tsfc = 3.5e-4 * ur.s / ur.m
rocket_full_thrust = 7600000 * ur.N

gravitational_constant = 6.674e-11 * ur.m ** 3 / (ur.kg * ur.s ** 2)

earth_mass = 5.98e24 * ur.kg
earth_diameter = 12700000 * ur.m
earth_equator_vel = 460 * ur.m / ur.s

position = np.array((0.0, earth_diameter.magnitude / 2.0)) * ur.m
velocity = np.array((0.0, 0.0)) * ur.m / ur.s
thrust_angle = 60.0 * ur.degree
thrust_direction = np.array((0.0, 0.0))

start_time = time.time() * ur.s
t = 0.0 * ur.s
d_t = 0.01 * ur.s

figure = plt.figure()
earth = plt.Circle((0, 0), float(earth_diameter.magnitude / 2.0), color = 'g')
figure.gca().add_artist(earth)

arrowplt = plt.arrow(0, 0, 0, 0)

def event_handler(event):
    global thrust_angle
    
    if event.key == ',':
        thrust_angle += 10.0 * ur.degree
    elif event.key == '.':
        thrust_angle -= 10.0 * ur.degree
    elif hasattr(event, 'button') and event.button == 1:
        if event.xdata < 0.0:
            thrust_angle += 10.0 * ur.degree
        else:
            thrust_angle -= 10.0 * ur.degree
            
figure.canvas.mpl_connect('key_press_event', event_handler)
figure.canvas.mpl_connect('button_press_event', event_handler)

while t < simulation_time:
    arrowplt.remove()
    
    new_t = time.time() * ur.s - start_time
    d_t = new_t - t
    t = new_t
    
    rocket_distance = np.sqrt(np.sum(position ** 2))
    
    force_of_gravity = (
        (gravitational_constant * earth_mass * rocket_mass)
        / (rocket_distance ** 2)
    ).to(ur.N)
    gravity_direction = -position / rocket_distance
    gravity_force = gravity_direction * force_of_gravity
    
    thrust_magnitude = rocket_full_thrust if rocket_fuel_mass > 0 * ur.kg else 0 * ur.N
    thrust_direction = np.array((np.cos(thrust_angle), np.sin(thrust_angle)))
    thrust = thrust_direction * thrust_magnitude
    d_mass = max(-rocket_tsfc * thrust_magnitude * d_t, -rocket_fuel_mass).to(ur.kg)
    
    rocket_fuel_mass += d_mass
    rocket_mass += d_mass
    
    sigma_forces = gravity_force + thrust
    acceleration = sigma_forces / rocket_mass
    velocity += acceleration * d_t
    position += velocity * d_t

    arrow_direction = (thrust_direction * arrow_length).to(ur.m).magnitude

    plt.ion()
    plt.grid(True)
    arrowplt = plt.arrow(
        position[0].to(ur.m).magnitude,
        position[1].to(ur.m).magnitude,
        arrow_direction[0],
        arrow_direction[1],
        width = arrow_width.to(ur.m).magnitude
    )
    
    plt.title(f"Fuel remaining: {rocket_fuel_mass.magnitude}kg")
    plt.xlabel(f"Time elapsed: {t.magnitude}s")
    plt.axis((-1e6, 1e6, 6e6, 7e6))
    
    figure.canvas.draw()
    figure.canvas.flush_events()