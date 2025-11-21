
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

# command to run label-studio
CMD ["label-studio", "start", "--host", "0.0.0.0", "--port", "8000"]