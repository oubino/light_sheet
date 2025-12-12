### Convert .czi to .zarr files ####

from bioio import BioImage
from bioio_ome_zarr.writers import OMEZarrWriter
import os

def main():

    files = os.listdir("data")
    files = [f for f in files if f.endswith(".czi")]

    if not os.path.exists("output/"):
        os.makedirs("output")
    
    if not os.path.exists("output/zarr"):
        os.makedirs("output/zarr")

    for f in files:

        f_path = f"data/{f}"
        f_name = f.rstrip(".czi")
        zarr_file = f"output/zarr/{f_name}.zarr"

        img = BioImage(f_path)

        print("File: ", f_name)
        print("Dims: ", img.dims)
        print("Channel order: ", img.dims.order)  # returns string "TCZYX"
        print("Size of X dimension: ", img.dims.X)  # returns size of X dimension
        print("Dimension sizes: ", img.shape)  # returns tuple of dimension sizes in TCZYX order
        print("Img scenes: ", img.scenes) # Get a list valid scene ids
        print("Current scene: ", img.current_scene) # Get the id of the current operating scene

        # --- Only look at one time point --- #
        assert img.dims.order == "TCZYX"
        assert len(img.scenes) == 1
        channels = None
        output = img.dask_data[0, :]

        writer = OMEZarrWriter(
            store=zarr_file,
            level_shapes=[output.shape],
            dtype=img.dtype,
            zarr_format=3,
            channels=channels,
            axes_names=["c", "z", "y", "x"],
            axes_types=["channel", "space", "space", "space"],
            axes_units=[None, "micrometer", "micrometer", "micrometer"],
        )

        writer.write_full_volume(output)


if __name__ == "__main__":
    main()