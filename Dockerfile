# Use an official Java runtime as a parent image
FROM openjdk:11

# Set the working directory in the container
WORKDIR /workspace

# Install required tools
RUN apt-get update && apt-get install -y wget git

# Clone the necessary directory from the GitHub repository
RUN git clone https://github.com/macster110/x3.git /workspace/x3

# Compile the Java code
RUN javac -cp /workspace/x3/X3/src org/pamguard/x3/sud/test/SudarFileTest.java

# Default command
CMD ["java", "-cp", "/workspace/x3/X3/src", "org.pamguard.x3.sud.test.SudarFileTest"]
