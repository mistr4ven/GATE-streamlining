from database import returnParticleValue

def do_transform(input_array):
    particles_simulated = 1e9
    particle_type = returnParticleValue("Y90_17G") 

    # divide every value in the array by the amount of particles simulated and then multiply by the particle type
    return (input_array/particles_simulated) * particle_type

