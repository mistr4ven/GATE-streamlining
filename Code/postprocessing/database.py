# This file is for a database of particles and their respective values, providing a clean way to access them

# add further particles here
particles = {
    "Y90_3G":3*1e9,
    "Y90_4G":4*1e9,
    "Y90_5G":5*1e9,
    "Y90_6G":6*1e9,
    "Y90_7G":7*1e9,
    "Y90_8G":8*1e9,
    "Y90_9G":9*1e9,
    "Y90_10G":10*1e9,
    "Y90_11G":11*1e9,
    "Y90_12G":12*1e9,
    "Y90_13G":13*1e9,
    "Y90_14G":14*1e9,
    "Y90_15G":15*1e9,
    "Y90_16G":16*1e9,
    "Y90_17G":17*1e9,
    "Y90_18G":18*1e9,
    "Y90_19G":19*1e9,
    "Y90_20G":20*1e9,
    "Ho166_1G":1*1e9,
    "Ho166_2G":2*1e9,
    "Ho166_3G":3*1e9,
    "Ho166_4G":4*1e9,
    "Ho166_5G":5*1e9,
    "Ho166_6G":6*1e9,
    "Ho166_7G":7*1e9,
    "Ho166_8G":8*1e9,
    "Ho166_9G":9*1e9,
    "Ho166_10G":10*1e9,
    "Ho166_11G":11*1e9,
    "Ho166_12G":12*1e9,
    "Ho166_13G":13*1e9,
    "Ho166_14G":14*1e9,
    "Ho166_15G":15*1e9,
    "Ho166_0G":0*1e9,
    "Y90_40": 1.33e+07,
    "Y90_225": 7.49e+07,
    "Y90_2500": 8.32e+08,
    "Ho166_240": 3.34e+07,
    "Ho166_375": 5.22e+07,  
}

def returnParticleValue(particletype):
    return particles[particletype]
    
