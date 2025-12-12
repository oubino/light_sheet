# Analysing cells from light-sheet data

## Environment

conda create -n light_sheet python=3.11
pip install bioio bioio-ome-tiff bioio-czi bioio-ome-zarr
pip install "napari[all]"
pip install matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cu126
pip install dask-image dask-jobqueue
pip install "bokeh>=3.1.0"

pip install edt
-- I had to install visual studio tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
pip install u-Segment3D

pip install cellpose[gui]

# You may need to install these...
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

## Remaining issues....

1. Initial training with CellSAM through Cellpose GUI, it was struggling to annotate the cells... therefore:
    a. Is cellpose the right architecture for these cells
    b. Does it just need further training
    c. Model = cyto2 seemed to work well initially, so could we retrain this model instead

2. Segment3d script amendment
    a. needs to be amended to take in the trained model from 2D training by changing the path to the model to be the custom trained tmodel
    b. need to work out how to do for a whole FOV... could either tile across the whole FOV or just apply to each of the pre-selected tiles/areas from before?

2. Which version/fork of u-Segment3D to install
4. Commit light sheet changes
8. Prepare handover incl. how to run on AIRE?
