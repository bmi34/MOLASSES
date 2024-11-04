#!/bin/bash

# Path to the vents file and output directory
VENTS_FILE="./inputs/vents_all.utm"
OUTPUT_DIR="./flow_outputs/flowF_AuckC"
CSV_CLEANER_SCRIPT="./convert_to_csv.py"
RASTER_CONVERTER_SCRIPT="./lava_flow_rasterised.py"

# Path to the virtual environment directory
VENV_DIR=~/molasses_env

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  echo "Virtual environment created at $VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
pip install --upgrade pip
pip install numpy pandas gdal

# Loop through each vent coordinate in vents_all.utm
while IFS= read -r line; do
  # Extract X and Y coordinates
  X=$(echo "$line" | awk '{print $1}')
  Y=$(echo "$line" | awk '{print $2}')
  
  # Update the vents file with current vent coordinates
  echo "$X $Y" > ./inputs/vents.utm

  # Run the MOLASSES model
  ./bin/molasses.ljc ./inputs/molasses_F.conf

  # Check if the flowF0 output file exists
  if [ -f "flowF0" ]; then
    # Define CSV output path
    output_csv="$OUTPUT_DIR/flowF_${X}_${Y}.csv"

    # Run the CSV cleaner script to create a clean CSV
    python3 "$CSV_CLEANER_SCRIPT" "flowF0" "$output_csv"

    # Convert the cleaned CSV to a raster file
    output_raster="${output_csv%.csv}.tif"
    python3 "$RASTER_CONVERTER_SCRIPT" "$output_csv" "$output_raster"

    echo "Raster created for $output_csv at $output_raster"
  else
    echo "Error: flowF0 file not found for vent at X:$X, Y:$Y"
  fi

done < "$VENTS_FILE"

# Deactivate the virtual environment
deactivate

echo "Batch conversion completed!"
