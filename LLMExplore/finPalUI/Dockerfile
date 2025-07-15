# pull python base image
FROM python:3.13

# copy application files
ADD /finchat_app /finchat_app

# specify working directory
WORKDIR /finchat_app

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# remove extra files to reduce image size
RUN rm requirements.txt

# expose port for application
EXPOSE 8001

# start fastapi application
CMD ["python", "main.py"]