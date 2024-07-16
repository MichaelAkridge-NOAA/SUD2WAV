# Use an official Java runtime as a parent image
FROM openjdk:11

# Set the working directory in the container
WORKDIR /workspace

# Install required tools
RUN apt-get update && apt-get install -y wget

# Download the Java files from the GitHub repository
RUN wget -P /workspace/org/pamguard/x3/sud/test https://raw.githubusercontent.com/macster110/x3/main/X3/src/org/pamguard/x3/sud/test/SudarFileTest.java \
    && wget -P /workspace/org/pamguard/x3/sud https://raw.githubusercontent.com/macster110/x3/main/X3/src/org/pamguard/x3/sud/SudFileExpander.java \
    && wget -P /workspace/org/pamguard/x3/sud https://raw.githubusercontent.com/macster110/x3/main/X3/src/org/pamguard/x3/sud/Chunk.java \
    && wget -P /workspace/org/pamguard/x3/sud https://raw.githubusercontent.com/macster110/x3/main/X3/src/org/pamguard/x3/sud/SudParams.java \
    && wget -P /workspace/org/pamguard/x3/utils https://raw.githubusercontent.com/macster110/x3/main/X3/src/org/pamguard/x3/utils/XMLUtils.java

# Compile the Java code
RUN javac -cp . org/pamguard/x3/sud/test/SudarFileTest.java

# Default command
CMD ["java", "org.pamguard.x3.sud.test.SudarFileTest"]
