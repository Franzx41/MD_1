#To build
# sudo docker build -t md_2 .
#To open jupyter
# sudo docker run -p 8888:8888 -v <"where you want to save your new notebooks(full path)">:/home/demo md_2

FROM ubuntu:19.04

##Set environment variables
## I do not know if it is really needed
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN pip3 install jupyter notebook

VOLUME /home/demo

WORKDIR /home/demo

ADD . /home/demo

# Start the jupyter notebook
ENTRYPOINT ["jupyter", "notebook", "--allow-root", "--ip=0.0.0.0"]



