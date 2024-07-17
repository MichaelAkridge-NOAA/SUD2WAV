import streamlit as st
import os
import subprocess
import pandas as pd
st.set_page_config(
    page_title="Bulk SUD to WAV Converter",
    page_icon="🎵",
)
def scan_sud_files(input_dir):
    if not os.path.exists(input_dir):
        st.error(f"Input directory does not exist: {input_dir}")
        return 0
    return len([f for f in os.listdir(input_dir) if f.endswith('.sud')])

def convert_sud_to_wav(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Initialize summary counters
    total_files = 0
    processed_files = 0
    failed_files = 0
    conversion_results = []

    sud_files = [f for f in os.listdir(input_dir) if f.endswith('.sud')]
    total_files = len(sud_files)

    progress_bar = st.progress(0)
    progress_text = st.empty()

    for i, sud_file in enumerate(sud_files):
        input_file_path = os.path.join(input_dir, sud_file)
        base_name = os.path.splitext(sud_file)[0]
        output_file_path = os.path.join(output_dir, f"{base_name}.wav")
        
        progress_text.text(f"🔄 Converting {sud_file} ({i+1}/{total_files})")
        
        result = subprocess.run([
            'java', 
            '-cp', '/workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar',
            'org.pamguard.x3.sud.ConvertSUDToWAV', 
            input_file_path, 
            output_file_path, 
            'verbose'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            processed_files += 1
            conversion_results.append({
                "File": sud_file,
                "Status": "Success",
                "Output Path": output_file_path
            })
        else:
            failed_files += 1
            conversion_results.append({
                "File": sud_file,
                "Status": "Failed",
                "Output Path": ""
            })
        
        progress_bar.progress((i+1) / total_files)

    summary = {
        "total_files": total_files,
        "processed_files": processed_files,
        "failed_files": failed_files,
        "conversion_results": conversion_results
    }

    return summary

# Sidebar
st.sidebar.title("Bulk SUD to WAV Converter 🎵")
st.sidebar.write("Convert your SUD files into WAV format.")

# Main content
st.title('Bulk SUD to WAV Converter 🎵')

input_directory = "/workspace/input_sud_files"
output_directory = "/workspace/output_wav_files"

if st.button('Scan for SUD Files'):
    num_files = scan_sud_files(input_directory)
    st.write(f"Found {num_files} SUD files in the input directory.")

if st.button('Convert 🛠️'):
    summary = convert_sud_to_wav(input_directory, output_directory)
    
    if summary:
        st.success('Conversion complete!')
        
        # Display conversion results
        st.write("### 📊 Summary:")
        st.write(f"**Total files:** {summary['total_files']}")
        st.write(f"**Successfully processed files:** {summary['processed_files']}")
        st.write(f"**Failed files:** {summary['failed_files']}")