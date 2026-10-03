# Use an official data science runtime as a parent image
FROM jupyter/scipy-notebook:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy your local notebook and files into the container
COPY . .

# Expose the default Jupyter port
EXPOSE 8888

# Start the Jupyter notebook server inside the container
CMD ["start-notebook.sh", "--NotebookApp.token=''"]