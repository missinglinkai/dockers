FROM debian:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-setuptools \
        python-scipy \
        python3 \
        python3-pip

RUN python -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install setuptools virtualenv
RUN python -m pip install setuptools virtualenv

ENV CAFFE_ROOT=/opt/caffe
WORKDIR $CAFFE_ROOT

# FIXME: use ARG instead of ENV once DockerHub supports this
ENV CLONE_TAG=rc4

RUN git clone -b ${CLONE_TAG} --depth 1 https://github.com/BVLC/caffe.git . && \
	cd python && for req in $(cat requirements.txt) pydot; do pip install $req; done

RUN mkdir build && cd build && \
    cmake -DCPU_ONLY=1 .. && \
    make -j"$(nproc)"

RUN apt-get install -y python python3

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

RUN python -m pip install https://s3.amazonaws.com/pytorch/whl/cu75/torch-0.1.9.post2-cp27-none-linux_x86_64.whl && \
	python -m pip install torchvision && \
	python -m pip install virtualenv

RUN python -m pip install keras tensorflow
RUN python3 -m pip install keras tensorflow

WORKDIR /workspace

RUN ln /dev/null /dev/raw1394

RUN $CAFFE_ROOT/data/mnist/get_mnist.sh && \
	$CAFFE_ROOT/examples/mnist/create_mnist.sh