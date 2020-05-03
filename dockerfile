FROM ubuntu:18.04

WORKDIR /home

RUN apt-get update && apt-get upgrade -y

# timezone setting
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
ENV TZ=Asia/Tokyo

# basic tools
RUN apt-get install -y wget curl sudo git vim

# build tools for python
RUN apt-get install -y build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev wget curl sudo

# build
RUN wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz \
&& tar xzf Python-3.7.4.tgz && cd Python-3.7.4 \
&& ./configure --enable-shared && make && make install \
&& sh -c "echo '/usr/local/lib' > /etc/ld.so.conf.d/custom_python3.conf" && ldconfig \
&& cd /home && rm -rf Python-3.7.4* \
&& ln -s /usr/local/bin/python3 /usr/local/bin/python \
&& ln -s /usr/local/bin/pip3 /usr/local/bin/pip

#MeCab
RUN apt-get install -y file mecab libmecab-dev mecab-ipadic-utf8 \
&& git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
&& cd mecab-ipadic-neologd \
&& bin/install-mecab-ipadic-neologd -y \
&& sed -i 's/dicdir.*/dicdir = \/usr\/lib\/x86_64-linux-gnu\/mecab\/dic\/mecab-ipadic-neologd/' /etc/mecabrc \
&& cd /home && rm -rf mecab-ipadic-neologd