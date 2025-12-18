### --- Load in and visualise napari --- ###
from bioio_ome_tiff.writers import OmeTiffWriter
import dask.array as da
import napari
import os
import zarr
import skimage.io as skio 

def main(argv=None):

    files = os.listdir("output/zarr")

    for f in files:
        
        f_name = f.removesuffix(".zarr")
        f_path = f"output/zarr/{f}"

        # load in zarr store
        store = zarr.open(f_path)

        # load in only image
        img = store['0']

        # create a dask array backed by the zarr store (lazy)
        img = da.from_zarr(img)

        # czyx -> zcyx
        img = img.transpose([1,0,2,3])

        OmeTiffWriter.save(
            img,
            f"output/tif/{f_name}_3D.tif",
            dim_order="ZCYX",
        )

        # czyx -> cyx, z=0
        img = img[0,:,:,:]

        OmeTiffWriter.save(
            img,
            f"output/tif/{f_name}_2D.tif",
            dim_order="CYX",
        )

if __name__ == "__main__":

    main()
