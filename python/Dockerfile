FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y \
    && apt-get -yq install nano tree python3-pip

RUN pip3 install tensorflow==2.4.0 Flask==1.1.2 \
    opencv-python==4.4.0.44 scikit-learn==0.23.2 \
    scipy==1.5.3 Pillow==8.0.1 h5py==2.10.0 \
    json5==0.9.5 matplotlib==3.3.2 pandas==1.1.3 \
    protobuf==3.13.0 regex==2020.10.23
    
WORKDIR /app

COPY . /app

EXPOSE 5000

CMD [ "python3", "app.py" ]