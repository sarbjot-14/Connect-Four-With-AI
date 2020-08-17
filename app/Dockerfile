# docker tutorial used: https://medium.com/@doedotdev/docker-flask-a-simple-tutorial-bbcb2f4110b5
#https://www.youtube.com/watch?v=Qw9zlE3t8Ko
# sudo docker build -t my_docker_flask:latest .
# docker run -d -p 5000:5000 my_docker_flask:latest
# docker-compose up

# got to http://0.0.0.0:5001/

FROM python:3-onbuild
COPY . /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "run.py"]


