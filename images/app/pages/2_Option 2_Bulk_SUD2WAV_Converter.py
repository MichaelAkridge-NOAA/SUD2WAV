import streamlit as st
import os
import subprocess
import re

st.set_page_config(
    page_title="Bulk SUD to WAV Converter",
    page_icon="🎵",
)

def remove_invalid_characters(xml_content):
    # Remove all non-printable characters except for newline, carriage return, and tab
    cleaned_content = re.sub(r'[^\x20-\x7E\x0A\x0D]', '', xml_content)
    return cleaned_content

def clean_xml_files_in_folder(folder_path):
    total_files = 0
    cleaned_files = 0
    failed_files = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            total_files += 1
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Read the XML file
                with open(file_path, 'r', encoding='utf-8') as file:
                    xml_content = file.read()
                
                # Clean the content
                cleaned_content = remove_invalid_characters(xml_content)
                
                # Write the cleaned content back to the same file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)
                
                cleaned_files += 1
            except Exception as e:
                failed_files += 1
                st.error(f"Failed to process {filename}: {e}")
    
    return {
        "total_files": total_files,
        "cleaned_files": cleaned_files,
        "failed_files": failed_files
    }

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
st.sidebar.write("Convert SUD files into WAV format.")

# Main content
st.title('Bulk SUD to WAV Converter 🎵')

input_directory = "/workspace/input_sud_files"
output_directory = "/workspace/output_wav_files"

if st.button('Scan for SUD Files'):
    num_files = scan_sud_files(input_directory)
    st.write(f"Found {num_files} SUD files in the input directory.")

if st.button('Convert Files 🛠️'):
    summary = convert_sud_to_wav(input_directory, output_directory)
    
    if summary:
        st.success('Conversion complete!')
        
        # Display conversion results
        st.write("### 📊 Summary:")
        st.write(f"**Total files:** {summary['total_files']}")
        st.write(f"**Successfully processed files:** {summary['processed_files']}")
        st.write(f"**Failed files:** {summary['failed_files']}")
        
        # Clean XML files in the output directory after conversion
        st.write("### 📊 Cleaning XML Files Step:")
        clean_summary = clean_xml_files_in_folder(output_directory)
        st.write("### 📊 XML Cleaning Summary:")
        st.write(f"**Total XML files:** {clean_summary['total_files']}")
        st.write(f"**Cleaned XML files:** {clean_summary['cleaned_files']}")
        st.write(f"**Failed XML files:** {clean_summary['failed_files']}")
