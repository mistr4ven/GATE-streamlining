import numpy as np
from pathlib import Path
import SimpleITK as sitk
from timer_deco import timer

def load_images(output_path, split, dummy_macro_file):

    # Create a Path object from the output path
    output_path = Path(output_path)
    dummy_macro_file = Path(dummy_macro_file)

    try:
        # Set the correct subdirectory
        split_path = output_path / f'split_{split}'
        # Load the image ending on *-Dose-Squared.raw in that subdirectory via simpleITK
        dose_squared_image = sitk.ReadImage(str(split_path / 'dose_actor-Dose-Squared.mhd'))
        # Load the image ending on *-Dose.raw in that subdirectory via simpleITK
        dose_image = sitk.ReadImage(str(split_path / 'dose_actor-Dose.mhd'))
        # Load the image ending on *-Edep.raw in that subdirectory via simpleITK
        edep_image = sitk.ReadImage(str(split_path / 'dose_actor-Edep.mhd'))
    except Exception as e:
        print(f"An error occurred while loading the images: {e}")
        exit(1)

    return dose_squared_image, dose_image, edep_image

def write_images(output_path, image, metadata, name, dummy_macro_file):
    
    # Create a Path object from the output path
    output_path = Path(output_path)
    dummy_macro_file = Path(dummy_macro_file)

    try:
        # Write the image to the merged subdirectory with the given name
        for key, value in metadata.items():
            image.SetMetaData(key, value)
        sitk.WriteImage(image, str(output_path / 'merged' / f'{dummy_macro_file.stem}_merged_{name}.mhd'), True) # the third argument sets output file compression to True/False
    except Exception as e:
        print(f"An error occurred while writing the images: {e}")
        exit(1)

@timer
def merge_images(output_path, splits, x_dim, y_dim, z_dim, particle_amount, dummy_macro_file):
    # define a zeroed numpy matrix for each image type of the given dimensions
    dose_squared = np.zeros((x_dim, y_dim, z_dim))
    dose = np.zeros((x_dim, y_dim, z_dim))
    edep = np.zeros((x_dim, y_dim, z_dim))

    metadata_dose_squared = None
    metadata_dose = None
    metadata_edep = None

    # loop over all splits
    for i in range(splits):
        # load the images
        dose_squared_image, dose_image, edep_image = load_images(output_path, i, dummy_macro_file)
        # get the numpy arrays of the images
        dose_squared_array = sitk.GetArrayFromImage(dose_squared_image)
        dose_array = sitk.GetArrayFromImage(dose_image)
        edep_array = sitk.GetArrayFromImage(edep_image)

        # get the metadata of the images if not already done for the later image creation
        if metadata_dose_squared is None:
            metadata_dose_squared = {key: dose_squared_image.GetMetaData(key) for key in dose_squared_image.GetMetaDataKeys()}
            metadata_dose = {key: dose_image.GetMetaData(key) for key in dose_image.GetMetaDataKeys()}
            metadata_edep = {key: edep_image.GetMetaData(key) for key in edep_image.GetMetaDataKeys()}

        # scale dose_array by the particle amount
        dose_array *= particle_amount
        # same with edep_array
        edep_array *= particle_amount

        # add the values of the current split to the total values
        dose_squared += dose_squared_array
        dose += dose_array
        edep += edep_array

    # compute the total events
    totalevents = splits * particle_amount
    
    # weighted average over the the dose
    dose_weightedaverage = dose / totalevents

    # weighted average over the edep
    edep_weightedaverage = edep / totalevents

    # weighted average divided by number of events per split 
    dose_all = dose_weightedaverage / particle_amount
    edep_all = edep_weightedaverage / particle_amount

    # compute the statictical uncertainty per voxel like in matlab skript
    # Compute statistical uncertainty per voxel
    stat_uncertainty_voxel = np.sqrt((1 / (totalevents - 1)) * (dose_squared / totalevents - np.square(dose_all)))


    #########################################################################
    # choose one of the methods below for the relative uncertainty          #
    #########################################################################

    ####### rel uncertainty in percent #######
    # # Compute relative uncertainty
    # rel_uncertainty = stat_uncertainty_voxel / dose_all * 100

    # # Handle NaN values (e.g., where Dose_all is zero)
    # rel_uncertainty = np.where(np.isnan(rel_uncertainty), 100, rel_uncertainty)
    ####### rel uncertainty in percent #######


    ####### rel uncertainty in values between 0 and 1 ######
    # # Compute relative uncertainty
    rel_uncertainty = stat_uncertainty_voxel / dose_all 

    # # Handle NaN values (e.g., where Dose_all is zero)
    rel_uncertainty = np.where(np.isnan(rel_uncertainty), 1, rel_uncertainty)
    ####### rel uncertainty in values between 0 and 1 ######

    #########################################################################

    # write the dose_squared to the merged subdirectory
    dose_squared_image = sitk.GetImageFromArray(dose_squared)
    write_images(output_path, dose_squared_image, metadata_dose_squared, 'Dose-Squared', dummy_macro_file)

    # write the dose to the merged subdirectory
    dose_image = sitk.GetImageFromArray(dose)
    write_images(output_path, dose_image, metadata_dose, 'Dose', dummy_macro_file)

    # write the edep to the merged subdirectory
    edep_image = sitk.GetImageFromArray(edep)
    write_images(output_path, edep_image, metadata_edep, 'Edep', dummy_macro_file)

    # write the dose_all to the merged subdirectory
    dose_all_image = sitk.GetImageFromArray(dose_all)
    write_images(output_path, dose_all_image, metadata_dose, 'Dose-All', dummy_macro_file)

    # write the edep_all to the merged subdirectory
    edep_all_image = sitk.GetImageFromArray(edep_all)
    write_images(output_path, edep_all_image, metadata_edep, 'Edep-All', dummy_macro_file)

    # write the statistical uncertainty to the merged subdirectory
    stat_uncertainty_image = sitk.GetImageFromArray(stat_uncertainty_voxel)
    write_images(output_path, stat_uncertainty_image, metadata_dose_squared, 'Stat-Uncertainty', dummy_macro_file)

    # write the relative uncertainty to the merged subdirectory
    rel_uncertainty_image = sitk.GetImageFromArray(rel_uncertainty)
    write_images(output_path, rel_uncertainty_image, metadata_dose_squared, 'Rel-Uncertainty', dummy_macro_file)

    # write the dose_weightedaverage to the merged subdirectory
    dose_weightedaverage_image = sitk.GetImageFromArray(dose_weightedaverage)
    write_images(output_path, dose_weightedaverage_image, metadata_dose, 'Dose-WeightedAverage', dummy_macro_file)

    # write the edep_weightedaverage to the merged subdirectory
    edep_weightedaverage_image = sitk.GetImageFromArray(edep_weightedaverage)
    write_images(output_path, edep_weightedaverage_image, metadata_edep, 'Edep-WeightedAverage', dummy_macro_file)
