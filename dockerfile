# Use an official data science runtime as a parent image
FROM jupyter/scipy-notebook:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy your local notebook and files into the container
COPY . .

# Install Python dependencies
RUN pip install kafka-python

# Expose the default Jupyter port
EXPOSE 8888

# Override entrypoint to prevent recursive start.sh
ENTRYPOINT [""]

# Start the Jupyter notebook server inside the container
CMD ["start-notebook.sh", "--NotebookApp.token=''"]