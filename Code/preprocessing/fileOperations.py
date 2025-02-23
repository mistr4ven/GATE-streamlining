from pathlib import Path
import random
from timer_deco import timer

# Create the output directory structure
@timer
def create_directory_structure(output_path, splits):

    # Create a Path object from the output path
    output_path = Path(output_path)

    # Create a directory using a relative path
    output_path.mkdir(parents=True, exist_ok=True)
    
    # create the macros subdirectoriy
    macro_path = output_path / 'macros'
    macro_path.mkdir(parents=True, exist_ok=True)

    # create the split subdirectories
    for i in range(splits):
        split_path = output_path / f'split_{i}'
        split_path.mkdir(parents=True, exist_ok=True)

    # create the merged subdirectory
    results_path = output_path / 'merged'
    results_path.mkdir(parents=True, exist_ok=True)

@timer
def write_macros(dummy_macro_file, output_path, splits, particle_amount, seedfile=''):

    # Create a Path object from the dummy macro file
    dummy_macro_file = Path(dummy_macro_file)
    # Create a Path object from the output path
    output_path = Path(output_path)

    # If a seed file is provided, read the seeds from the file
    if seedfile != '':
        try:
            with open(seedfile, 'r') as f:
                seeds = f.readlines()
        except FileNotFoundError:
            print(f"File {seedfile} not found")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        # if the amount of seeds is not equal to the amount of splits, print an error
        if len(seeds) != splits:
            print(f"Amount of seeds ({len(seeds)}) does not match the amount of splits ({splits})")
            return
    else:
        # Create an instance of the Mersenne Twister random generator
        mt = random.Random()
        # Generate the seeds using the Mersenne Twister instance
        seeds = [mt.randint(0, 100000) for i in range(splits)]

        # check that no duplicates are present
        while (len(seeds) != len(set(seeds))):
            seeds = [mt.randint(0, 100000) for i in range(splits)]
            
    # Create a Path object for the macro output directory 
    macro_path = output_path / 'macros'

    # Check if the folder exists and delete .mac files if any
    if macro_path.exists() and macro_path.is_dir():
        for file in macro_path.glob('*.mac'):
            print(f"Deleting {file}")
            file.unlink()  

    # loop over all splits
    for i in range(splits):
        # Read the dummy macro file
        try:
            with open(dummy_macro_file, 'r') as f:
                macro = f.read()
        except FileNotFoundError:
            print(f"File {dummy_macro_file} not found")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        # Set the output of the stat actor if that pattern is found in the macro
        if '<STAT_ACTOR>' in macro:
            macro = macro.replace('<STAT_ACTOR>', f'{output_path}/split_{i}/stat_actor.txt')
        else:
            print("Pattern <STAT_ACTOR> not found in the macro file")
            return

        # Set the output of the dose actor if that pattern is found in the macro
        if '<DOSE_ACTOR>' in macro:
            macro = macro.replace('<DOSE_ACTOR>', f'{output_path}/split_{i}/dose_actor.mhd')
        else:
            print("Pattern <DOSE_ACTOR> not found in the macro file")
            return

        # Set the amount of particles to be simulated if that pattern is found in the macro
        if '<NUMBER_OF_PARTICLES>' in macro:
            macro = macro.replace('<NUMBER_OF_PARTICLES>', f'{particle_amount}')
        else:
            print("Pattern <NUMBER_OF_PARTICLES> not found in the macro file")
            return

        # Set the seed to one of the seeds if that pattern is found in the macro
        if '<SEED>' in macro:
            macro = macro.replace('<SEED>', f'{seeds[i]}')
        else:
            print("Pattern <SEED> not found in the macro file")
            return

        # Write the macro to the macro output directory
        macro_path = output_path / 'macros' / f'{dummy_macro_file.stem}_split_{i}.mac'
        try:
            with open(macro_path, 'w') as f:
                f.write(macro)
        except Exception as e:
            print(f"An error occurred writing the {i}th macro file: {e}")
            return

    # If no seedfile was provided, write the seeds to a file
    if seedfile == '':
        seedfile = output_path / 'macros' / '.seeds.txt'
        try:
            with open(seedfile, 'w') as f:
                for seed in seeds:
                    f.write(f'{seed}\n')
        except Exception as e:
            print(f"An error occurred writing the .seeds file: {e}")
            return
