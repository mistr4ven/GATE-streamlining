from database import returnParticleValue

def do_transform(input_array):
    particle_type = returnParticleValue("Ho166_240") 

    return input_array * particle_type

