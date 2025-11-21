
# create a docker file to use python 3.11
FROM python:3.11-slim

# set the working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt .

# install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code
COPY . .

# expose the port
EXPOSE 8000

# print running python script


# execute the prepare_dataset script
RUN echo "Running label_studio.py script"
RUN python prepare_dataset.py

# run the label_studio.py script
RUN echo "Starting Label Studio"
CMD ["python", "label_studio.py"]