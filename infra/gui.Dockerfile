# Dockerfile-gui

# Use an official Python runtime as a parent image
FROM python:3.9.13

# Set the working directory in the container to /src
WORKDIR /src

# Add the GUI directory contents into the container at /src/gui
ADD ../src/gui /src/gui/

# Copy the requirements.txt file into the container at /src/
COPY ../requirements.txt /src/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the app when the container launches
CMD ["chainlit", "run", "--port", "8080", "gui/web_app.py"]