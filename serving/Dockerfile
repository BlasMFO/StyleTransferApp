FROM tensorflow/serving:2.4.0-rc4

RUN apt-get update && apt-get upgrade -y \
    && apt-get -yq install nano tree tar wget

RUN mkdir /models/tftransfer && mkdir /models/tftransfer/1 && \
    wget "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2?tf-hub-format=compressed" && \
    tar -C /models/tftransfer/1 -zxvf ./2* && rm -f 2*

EXPOSE 8500 8501