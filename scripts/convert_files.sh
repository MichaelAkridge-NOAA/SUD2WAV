#!/bin/bash
set -e

# Create output directory if it doesn't exist
mkdir -p /workspace/output_wav_files

# Process each .sud file in the input directory
for sud_file in /workspace/input_sud_files/*.sud; do
  # Extract the base name of the file (without directory and extension)
  base_name=$(basename "$sud_file" .sud)
  # Define the output WAV file path
  wav_file="/workspace/output_wav_files/${base_name}.wav"
  # Log the conversion process
  echo "Converting $sud_file to $wav_file"
  # Run the Java application to convert the file
  java -cp /workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar /workspace/scripts/SudarFileTest "$sud_file" "$wav_file"
  # Log if conversion was successful
  if [ -f "$wav_file" ]; then
    echo "Successfully converted $sud_file to $wav_file"
  else
    echo "Failed to convert $sud_file"
  fi
done

