import streamlit as st
import os
import subprocess
import pandas as pd

st.set_page_config(
    page_title="SUD2WAV",
    page_icon="🎵",
)

# Sidebar
st.sidebar.title("SUD to WAV Converter 🎵")
st.sidebar.write("Convert your SUD files into WAV format.")

# Main content
st.title('SUD to WAV Converter 🎵')
st.markdown(
    """
    A Python web app to convert .sud files to .wav files using a Docker & Java-based conversion library.
    ## **👈 Select a converter from the sidebar** 
    """
)

# Use columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Option 1: Regular Converter")
    st.markdown(
        """
        - Drag and drop files to be converted
        - Detailed logs and conversion reports
        """
    )

with col2:
    st.subheader("Option 2: Bulk Converter")
    st.markdown(
        """
        - Scans mounted input folder
        - Designed to convert multiple files
        """
    )

st.markdown("### Data File Info")

st.write("""
- **.sud** files: Raw downloaded files. Compressed for storage or sending of complete recordings.
- **.wav** files: Microsoft WAV format files. Can be opened by any media player, Matlab, etc.
- **.xml** files: Contain metadata such as date recorded, gain setting, etc.
""")

st.markdown("### Want to learn more?")
st.markdown(
    """
    - Check out the [Github Repo](https://github.com/MichaelAkridge-NOAA/SUD2WAV)
    """
)

# Footer
st.markdown("---")
st.markdown(
    """
    **Developed by [Michael Akridge]**  
    For inquiries, please contact [michael.akridge@noaa.gov](mailto:michael.akridge@noaa.gov)
    """
)
