# Use Amazon Corretto as a parent image or any other Open JDK image
FROM amazoncorretto:11 as java

# Use any Python image for Streamlit app
FROM python:3.8-slim as python

# Copy the entire Java installation from the Java stage
COPY --from=java /usr/local /usr/local
COPY --from=java /usr/lib/jvm /usr/lib/jvm

# Set the working directory in the container
WORKDIR /workspace

# Install required tools
RUN apt-get update && apt-get install -y \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Streamlit
RUN pip install streamlit

# Clone your fork of the repository
RUN git clone https://github.com/MichaelAkridge-NOAA/x3.git /workspace/x3

# Download required libraries
RUN wget -P /workspace/lib https://repo1.maven.org/maven2/commons-io/commons-io/2.11.0/commons-io-2.11.0.jar \
    && wget -P /workspace/lib https://repo1.maven.org/maven2/com/google/guava/guava/30.1.1-jre/guava-30.1.1-jre.jar

# Copy the scripts and app directory into the container
COPY app.py /workspace/app.py

# Ensure javac is in the PATH
ENV PATH="/usr/lib/jvm/java-11-amazon-corretto/bin:${PATH}"

# Compile the Java code from your repository
RUN javac -cp /workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar /workspace/x3/X3/src/org/pamguard/x3/sud/ConvertSUDToWAV.java

# Expose the Streamlit port
EXPOSE 8501

# Default command to run the Streamlit app
CMD ["streamlit", "run", "/workspace/app.py"]

