from bioio import BioImage
from bioio_ome_zarr.writers import OMEZarrWriter
from cellpose.contrib.distributed_segmentation import process_block, distributed_eval
import dask.array as da
import os
import napari
import matplotlib.pyplot as plt
import time
import zarr

# ---- parameters -----

#file_path = "D:/Post-processed image subsets/WHOLE HEART POST-PROCESSED/018038 EC2-01.czi"

file_name = "ScanA_30-Lattice Lightsheet-04"
input_czi_file = os.path.join("D:/Natalia test data for Oli/Human Heart - 7.028/", file_name + ".czi")
zarr_file = f"sandpit/{file_name}.zarr"

convert_czi_to_zarr = False
visualise_in_napari = False
zero_shot_segment = True

# ---- Convert czi to zarr -----

if convert_czi_to_zarr:
    img = BioImage(input_czi_file)

    print("Dims: ", img.dims)
    print("Channel order: ", img.dims.order)  # returns string "TCZYX"
    print("Size of X dimension: ", img.dims.X)  # returns size of X dimension
    print("Dimension sizes: ", img.shape)  # returns tuple of dimension sizes in TCZYX order
    print("Img scenes: ", img.scenes) # Get a list valid scene ids
    print("Current scene: ", img.current_scene) # Get the id of the current operating scene

    assert img.dims.order == "TCZYX"
    assert len(img.scenes) == 1
    channels = None

    output = img.dask_data[0, [0,2], :]

    writer = OMEZarrWriter(
        store=zarr_file,
        level_shapes=[output.shape],
        dtype=img.dtype,
        zarr_format=3,  # 2 for Zarr v2
        channels=channels,
        axes_names=["c", "z", "y", "x"],
        axes_types=["channel", "space", "space", "space"],
        axes_units=[None, "micrometer", "micrometer", "micrometer"],
    )

    writer.write_full_volume(output)

# ------- Load in an image and visualise --------

if visualise_in_napari:

    # load in zarr store
    store = zarr.open(zarr_file)

    # load in only image
    img = store['0']

    # create a dask array backed by the zarr store (lazy)
    img = da.from_zarr(img)

    # visualise in napari
    napari.imshow(
        x,
        contrast_limits=[0, 5000],
    )
    napari.run()


# ------ Zero-shot segment the cells -----------

if zero_shot_segment:

    # load in zarr store
    store = zarr.open(zarr_file)

    # load in only image
    img = store['0']

    print(img.shape)

    # returns out-of-memory 4D dask array

    #img_subset = img[0,[0,2],:]

    # create a dask array backed by the zarr store (lazy)
    #x = da.from_zarr(img)

    # do fancy indexing lazily (no data read now)
    #subset = x[0, [0, 2], :]

    #print(type(subset))        # should be <class 'dask.array.core.Array'>
    #print(subset)              # shows lazy 
    
    print('here')

    # parameterize cellpose however you like
    model_kwargs = {
        'gpu':True, 
        'pretrained_model':'cpsam', 
        'model_type': None, 
    }
    

    eval_kwargs = {
        'diameter':30,
        'z_axis':1,
        'channel_axis':0,
        'do_3D':True,
    }

    # define a crop as the distributed function would
    starts = (16, 128, 128)
    blocksize = (32, 256, 256)
    overlap = 60
    crop = tuple(slice(s-overlap, s+b+overlap) for s, b in zip(starts, blocksize))

    # call the segmentation
    segments, boxes, box_ids = process_block(
        block_index=(0, 0, 0),  # when test_mode=True this is just a dummy value
        crop=crop,
        input_zarr=img,
        model_kwargs=model_kwargs,
        eval_kwargs=eval_kwargs,
        blocksize=blocksize,
        overlap=overlap,
        output_zarr=None,
        test_mode=True,
    )

    print(segments, boxes, box_ids)

# ------ Manually annotate data ------



# ------ Train a classifier --------


# ------ Generate cell segmentation -------



# ------ Analyse the cells -----------




