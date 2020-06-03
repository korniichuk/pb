# Name: korniichuk/pb
# Short Description: Pitney Bowes
# Full Description: Solution for Pitney Bowes's recruitment test
# Version: 0.1a4
# Owner: Ruslan Korniichuk

FROM ubuntu:18.04

MAINTAINER Ruslan Korniichuk <ruslan.korniichuk@gmail.com>

USER root

# 1. OS
# Retrieve new lists of packages
ENV OS_REFRESHED_AT 2020-06-02
RUN apt-get -qq update # -qq -- no output except for errors

# 2. APT
# Install wget
ENV APT_REFRESHED_AT 2020-06-02
RUN apt-get -qq update \
        && apt-get install -y wget \
        && apt-get clean

# 3. PYTHON+PIP
# Install python3, python3-dev
ENV PYTHON_REFRESHED_AT 2020-06-02
RUN apt-get -qq update \
        && apt-get install -y python3 python3-dev \
        && apt-get clean
# Download 'get-pip.py' file to '/tmp' directory
ENV PIP_REFRESHED_AT 2020-06-02
RUN wget --directory-prefix /tmp https://bootstrap.pypa.io/get-pip.py
# Install pip
RUN python3 /tmp/get-pip.py
# Remove '/tmp/get-pip.py' file
RUN rm /tmp/get-pip.py

# 4. SECURITY
# Add new 'pb' user
RUN useradd -c "Pitney Bowes" -m -s /bin/bash pb
# Change password for 'pb' user
RUN echo "pb:pitneybowes" | chpasswd

USER pb

# 5. REQUIREMENTS
# Copy local 'requirements.txt' to image
COPY requirements.txt /tmp/requirements.txt
# Install Python packages
ENV REQUIREMENTS_REFRESHED_AT 2020-06-02
RUN pip3 install --upgrade --user --requirement /tmp/requirements.txt

USER root

# Remove 'requirements.txt' file
RUN rm /tmp/requirements.txt

# 6. FILE STRUCTURE
# Create dir for Python code
RUN mkdir --parents /opt/pb/bin/
RUN chown pb:pb /opt/pb/bin/
# Create dir for logger
RUN mkdir /var/log/pb/
RUN chown pb:pb /var/log/pb/

USER pb

# 7. PYTHON CODE
# Copy local 'data_analysis.py' to image
COPY data_analysis.py /opt/pb/bin/data_analysis.py
# Copy local 'pypandas.py' to image
COPY pypandas.py /opt/pb/bin/pypandas.py
# Copy local 'pys3.py' to image
COPY pys3.py /opt/pb/bin/pys3.py
# RUN Python scipt
CMD python3 /opt/pb/bin/data_analysis.py --db $db --s3_bucket $s3_bucket
