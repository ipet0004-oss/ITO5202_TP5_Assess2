# Use Jupyter scipy notebook as parent image
FROM jupyter/scipy-notebook:latest

# Switch to root to install Java
USER root

# Install Java required by PySpark
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Return to normal Jupyter user
USER ${NB_UID}

# Set working directory
WORKDIR /usr/src/app

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir pyspark kafka-python

# Expose Jupyter port
EXPOSE 8888

# Override entrypoint
ENTRYPOINT [""]