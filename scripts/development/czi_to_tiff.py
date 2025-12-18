from bioio import BioImage
from bioio_ome_tiff.writers import OmeTiffWriter
import os

def main():

    files = os.listdir("data")
    files = [f for f in files if f.endswith(".czi")]

    if not os.path.exists("output/"):
        os.makedirs("output")
    
    if not os.path.exists("output/tif"):
        os.makedirs("output/tif")

    for f in files:

        f_path = f"data/{f}"
        f_name = f.rstrip(".czi")
        zarr_file = f"output/tif/{f_name}.tif"

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
        output = img.dask_data[0, :]

        OmeTiffWriter.save(
            output,
            zarr_file,
            dim_order="CZYX",
        )



if __name__ == "__main__":
    main()