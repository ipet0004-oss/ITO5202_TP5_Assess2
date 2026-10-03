Assessment 2: Machine learning and real-time streaming
ITO5202 TP2 2026

Name: Iliana Peters
Student Number: 35723483

Project Overview:
This project uses data collected from Uber rides during 2024. The business goal of this project is to create a model that would predict what rating the customer gave to the driver based on the available ride data. Feature engineering was completed to transform categorical data into numerical to aid in modelling but also to determine suitable features from dataset to be used in the model. After an ideal model was chosen based on appropriate evaluations, a simulated streaming of live data was completed using Kafka. This live data was then run through the ideal model and the predictions were compared to the initial predictions found in the modelling process. A final reflection was completed to explain reasoning, highlight challenges and how the process would deal with larger data volumes.

Execution Steps for initial setup of docker container and using producer in VS Code:
1. A dockerfile is used to help setup the containers and ensure all dependencies are correct. Additionally this code is relevant for using VS Code and a mac environment.
2. Intsall the Docker extension
3. In terminal create pyspark container: docker build -t ito5202-pyspark-fixed -f dockerfile 
4. Create and start zookeeper container: docker run -d \
  --name zookeeper \
  --network ito5202 \
  -e ALLOW_ANONYMOUS_LOGIN=yes \
  monashfit/fit5202-zookeeper
5. Create and start kafka container: docker run -d \
  --name kafka \
  --network ito5202 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_HOST_NAME=kafka \
  monashfit/fit5202-kafka
6. Create and start pyspark container: docker run -d \
  --name pyspark \
  --network ito5202 \
  -p 8888:8888 \
  -v "$(pwd):/home/jovyan/work" \
  ito5202-pyspark-fixed \
  start-notebook.sh \
  --NotebookApp.token='' \
  --NotebookApp.password=''
  7. Enter pyspark container: docker exec -it pyspark bash
  8. In terminal navigate to container folder: cd /home/jovyan/work
  9. Run python code from this location: python producer.py
  10. In terminal use exit to exit the container