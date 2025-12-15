### --- Prepare for cellpose segmentation --- ###
import dask.array as da
from bioio_ome_tiff.writers import OmeTiffWriter
import os
import numpy as np
import zarr

def main(argv=None):

    n_img = 50
    img_size = 1024
    
    # Select random regions of small-ish size from the bounding boxes at random z
    file_folder = "output/zarr"
    files = os.listdir(file_folder) 

    # generate output folder if doesn't exist
    if not os.path.exists("output/cellpose"):
        os.makedirs("output/cellpose")

    for f in files:
        
        # file name
        f_name = f.removesuffix(".zarr")

        # load in zarr store
        f_path = os.path.join(file_folder, f)
        store = zarr.open(f_path)
        img = store['0']
        img = da.from_zarr(img)

        boxes_file = f"output/boxes/{f}.npy"
        boxes = np.load(boxes_file)

        # no. of tiles per box to generate
        tiles_per_box = int(n_img / len(boxes))

        # z size
        z_size = img.shape[1]

        for b in boxes:

            ymin = int(b[:,2].min())
            ymax = int(b[:,2].max())
            xmin = int(b[:,3].min())
            xmax = int(b[:,3].max())

            rng = np.random.default_rng()
           
            xs = rng.integers(low=xmin, high=xmax - img_size, size=tiles_per_box)
            ys = rng.integers(low=ymin, high=ymax - img_size, size=tiles_per_box) 
            zs = rng.integers(low=0, high=z_size, size=tiles_per_box) 

            for x, y, z in zip(xs, ys, zs):

                # generate 2d view of the data
                # ignore nuclear channel....
                tile = img[0, z, y:y+img_size, x:x+img_size]

                # save as .tif to cellpose folder
                OmeTiffWriter.save(
                    tile,
                    f"output/cellpose/{f_name}_2Dtile_xyz_{x}_{y}_{z}.tif",
                    dim_order="YX",
                )  
       

if __name__ == "__main__":

    main()
