# Analysing cells from light-sheet data

## Environment

conda create -n light_sheet python=3.11
pip install bioio bioio-ome-tiff bioio-czi bioio-ome-zarr
pip install "napari[all]"
pip install matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cu126
pip install git+https://www.github.com/mouseland/cellpose.git
pip install dask-image dask-jobqueue

pip install "bokeh>=3.1.0"

pip install edt
-- I had to install visual studio tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
pip install u-Segment3D

git clone https://github.com/MouseLand/cellpose.git
cd cellpose
pip install -e .


pip install PyQt6
pip install pyqtgraph

## Set-up

1. Clone this repository

2. Move your .czi data into the data/ folder


## Workflow

1. Convert .czi to .zarr files

    ``` 
    python scripts/czi_to_zarr.py
    ```

2. Visualise files

    ``` 
    python scripts/visualise_zarr.py
    ```

    Select regions with clearly visible cells by adding a shapes layer and placing rectangles over these regions

3. Prepare for cellpose
    
    ```
    python scripts/prepare_for_cellpose.py
    ```

4. Train 2D Cellpose

    ``` 
    cellpose
    ```

    Use the cellpose GUI to load in these images, segment and create a model
    
    1. Open up the GUI with above line
    2. Change the diameter of cellopse to match the cells
    3. Open up each image and add labels
    4. Then click models > train_new_model

5. Evaluate 2D and convert to 3D using u-Segment3D

    ```
    python scripts/segment3d.py
    ```

    Load in the trained 2D model and generate 3D segmentation for the rectangle regions
    Tile data to make this tractable

6. Analyse cells

    ```
    python scripts/analyse_cells.py
    ```

## To do

1. Amend segment3d script
    - take in the trained model
    - do for each tile? or tile a whole box?
    - compare with original script to see how has changed...

1. Which version/fork of cellpose to install
2. Which version/fork of u-Segment3D to install
3. Commit cellpose changes
4. Commit light sheet changes
5. Commit unet3d changes
6. Change how to install instructions
7. Test run the whole thing
8. Prepare handover incl. how to run on AIRE?
9. Flag issue that usegment3d not 3d compatible