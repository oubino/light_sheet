# Analysing cells from light-sheet data

## Environment

conda create -n light_sheet python=3.11
pip install bioio bioio-ome-tiff bioio-czi bioio-ome-zarr
pip install "napari[all]"
pip install matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cu126
pip install git+https://www.github.com/mouseland/cellpose.git
pip install dask-image dask-jobqueue

## Workflow

1. Segment cells



2. Analyse cells