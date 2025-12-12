### --- Load in and visualise napari --- ###
from bioio_ome_zarr.writers import OMEZarrWriter
import dask.array as da
import napari
import numpy as np
import os
import zarr

def main(argv=None):

    files = os.listdir("output/zarr")

    for f in files:
        
        f_name = f.removesuffix(".zar")
        f_path = f"output/zarr/{f}"

        # load in zarr store
        store = zarr.open(f_path)

        # load in only image
        img = store['0']

        # create a dask array backed by the zarr store (lazy)
        img = da.from_zarr(img)
    
        # visualise in napari
        viewer = napari.Viewer()
        viewer.add_image(
            img,
            contrast_limits=[0, 5000],
        )

        # visualise bounding boxes if already present
        boxes_file = f"output/boxes/{f_name}.npy"
        if os.path.exists(boxes_file):
            boxes = np.load(boxes_file)
            viewer.add_shapes(boxes, 
                              name="Shapes",
                              shape_type="rectangle")

        napari.run()

        # save bounding boxes if present
        try:
            boxes = viewer.layers["Shapes"].data

            print(boxes)


            if not os.path.exists("output/boxes"):
                os.makedirs("output/boxes")

            np.save(
                boxes_file,
                boxes,
            )

        except KeyError:
            print("No bounding boxes present!")

if __name__ == "__main__":

    main()
