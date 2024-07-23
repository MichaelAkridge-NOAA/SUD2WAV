# clean_xml_files.py
import os
import re

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
                print(f"Failed to process {filename}: {e}")
    
    return {
        "total_files": total_files,
        "cleaned_files": cleaned_files,
        "failed_files": failed_files
    }

if __name__ == "__main__":
    folder_path = "/workspace/output_wav_files"
    summary = clean_xml_files_in_folder(folder_path)
    print("### 📊 XML Cleaning Summary:")
    print(f"**Total XML files:** {summary['total_files']}")
    print(f"**Cleaned XML files:** {summary['cleaned_files']}")
    print(f"**Failed XML files:** {summary['failed_files']}")
