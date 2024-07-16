# Use an official Java runtime as a parent image
FROM openjdk:11

# Set the working directory in the container
WORKDIR /workspace

# Install required tools
RUN apt-get update && apt-get install -y wget git

# Clone the necessary directory from the GitHub repository
# RUN git clone https://github.com/macster110/x3.git /workspace/x3
RUN git clone https://github.com/MichaelAkridge-NOAA/x3.git /workspace/x3


# Download required libraries
RUN wget -P /workspace/lib https://repo1.maven.org/maven2/commons-io/commons-io/2.11.0/commons-io-2.11.0.jar \
    && wget -P /workspace/lib https://repo1.maven.org/maven2/com/google/guava/guava/30.1.1-jre/guava-30.1.1-jre.jar

# Copy the scripts directory into the container
COPY scripts /workspace/scripts

# Make the script executable
RUN chmod +x /workspace/scripts/convert_files.sh

# Compile the Java code
RUN javac -cp /workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar /workspace/x3/X3/src/org/pamguard/x3/sud/test/SudarFileTest.java

# Default command
CMD ["java", "-cp", "/workspace/x3/X3/src:/workspace/lib/commons-io-2.11.0.jar:/workspace/lib/guava-30.1.1-jre.jar", "org.pamguard.x3.sud.test.SudarFileTest"]

