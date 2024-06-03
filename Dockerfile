# Use the official Apache Airflow image as a parent image
FROM apache/airflow:2.9.1-python3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Specify the command to run on container start
CMD ["airflow", "webserver"]
