from database import returnParticleValue

def do_transform(input_array):
    particle_type = returnParticleValue("Y90_40") 

    return input_array * particle_type

