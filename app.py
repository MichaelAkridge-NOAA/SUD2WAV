import streamlit as st
import os
import subprocess

def convert_sud_to_wav(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each .sud file in the input directory
    converted_files = []
    for sud_file in os.listdir(input_dir):
        if sud_file.endswith('.sud'):
            input_file_path = os.path.join(input_dir, sud_file)
            base_name = os.path.splitext(sud_file)[0]
            output_file_path = os.path.join(output_dir, f"{base_name}.wav")
            
            # Log the conversion process
            st.write(f"🔄 Converting {input_file_path} to {output_file_path}")
            
            # Run the Java application to convert the file
            result = subprocess.run([
                'java', 
                '-cp', '/workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar',
                'org.pamguard.x3.sud.ConvertSUDToWAV', 
                input_file_path, 
                output_file_path, 
                'verbose'
            ], capture_output=True, text=True)
            
            converted_files.append((sud_file, result.stdout, result.stderr, input_file_path, output_file_path))

    return converted_files

# Sidebar
st.sidebar.title("SUD to WAV Converter 🎵")
st.sidebar.write("Upload your SUD files to convert them into WAV format.")
st.sidebar.markdown("[SUD2WAV - GitHub Repository](https://github.com/MichaelAkridge-NOAA/SUD2WAV)")

# Main content
st.title('SUD to WAV Converter 🎵')

uploaded_files = st.file_uploader("Choose SUD files", accept_multiple_files=True, type=['sud'])
output_directory = '/workspace/output_wav_files'

if uploaded_files:
    st.write("### 📂 Files to be processed:")
    input_dir = '/workspace/input_sud_files'
    os.makedirs(input_dir, exist_ok=True)
    
    file_details = []
    for uploaded_file in uploaded_files:
        file_details.append([uploaded_file.name, "Pending"])
        with open(os.path.join(input_dir, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
    
    st.table(file_details)
    
    if st.button('Convert 🛠️'):
        converted_files = convert_sud_to_wav(input_dir, output_directory)
        
        st.success('Conversion complete!')
        
        # Display conversion results
        st.write("### 📁 Conversion Results:")
        for file_name, stdout, stderr, input_path, output_path in converted_files:
            with st.expander(f"🔊 {file_name}"):
                st.write("### 📄 Conversion Output:")
                st.text(stdout)
                st.write("### ⚠️ Conversion Errors (if any):")
                st.text(stderr)
        
        # List the converted files
        output_files = os.listdir(output_directory)
        st.write("### 📁 Converted Files:")
        st.table([[file] for file in output_files])
