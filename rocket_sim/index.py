import time
import numpy as np
from matplotlib import pyplot as plt
import pint

ur = pint.UnitRegistry()

arrow_length = 50 * ur.km
arrow_width= 30 * ur.km
simulation_time = 360000000 * ur.s
time_warp = 16

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
thrust_angle = 90.0 * ur.degree
thrust_direction = np.array((0.0, 0.0))

figure = plt.figure()
earth = plt.Circle((0, 0), float(earth_diameter.magnitude / 2.0), color = 'g')
figure.gca().add_artist(earth)

arrowplt = plt.arrow(0, 0, 0, 0)

def event_handler(event):
    global thrust_angle, time_warp
    
    if event.key == ',':
        thrust_angle += 10.0 * ur.degree
    elif event.key == '.':
        thrust_angle -= 10.0 * ur.degree
    elif event.key == '\'':
        time_warp += 1
    elif event.key == ';':
        time_warp -= 1
    elif hasattr(event, 'button') and event.button == 1:
        if event.xdata < 0.0:
            thrust_angle += 10.0 * ur.degree
        else:
            thrust_angle -= 10.0 * ur.degree
    
    time_warp = max(0, time_warp)
            
figure.canvas.mpl_connect('key_press_event', event_handler)
figure.canvas.mpl_connect('button_press_event', event_handler)

last_time = time.time() * ur.s
t = 0.0 * ur.s
d_t = 0.0 * ur.s

while t < simulation_time:
    arrowplt.remove()
    
    # crash into Earth detection
    rocket_distance = np.sqrt(np.sum(position ** 2))
    if t > 0 and rocket_distance <= earth_diameter / 2: velocity = np.array((0.0, 0.0)) * ur.m / ur.s
    
    new_time = time.time() * ur.s
    d_t = new_time - last_time
    d_t *= time_warp
    last_time = new_time
    t += d_t
    
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
    
    screenspace_x = max(4 * (rocket_distance - earth_diameter / 2), earth_diameter / 4)
    screenspace_y = screenspace_x * 3 / 4
    
    plt.title(f"Fuel remaining: {round(rocket_fuel_mass.magnitude)}kg")
    plt.xlabel(f"Time elapsed: {round(t.magnitude * 100) / 100}s (x{time_warp} time warp)")
    plt.axis((
        position[0].magnitude - screenspace_x.magnitude,
        position[0].magnitude + screenspace_x.magnitude,
        position[1].magnitude - screenspace_y.magnitude,
        position[1].magnitude + screenspace_y.magnitude
    ))
    
    print(round(velocity[1]), round(position[1]))
    
    figure.canvas.draw()
    figure.canvas.flush_events()