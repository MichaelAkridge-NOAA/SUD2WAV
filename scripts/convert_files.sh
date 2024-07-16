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
  # Run the Java application to convert the file
  java -cp /workspace/x3/X3/src org.pamguard.x3.sud.test.SudarFileTest "$sud_file" "$wav_file"
done

