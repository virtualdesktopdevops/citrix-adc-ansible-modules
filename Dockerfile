FROM alpine:3.10

ENV ANSIBLE_VERSION=2.9.2

# Install Python3 and Ansible
RUN set -xe \
    && echo "****** Install system dependencies ******" \
    && apk add --no-cache --progress python3 openssl ca-certificates git openssh sshpass \
	  && apk --update add --virtual build-dependencies python3-dev libffi-dev openssl-dev build-base \
	  && echo "****** Install ansible and python dependencies ******" \
    && pip3 install --upgrade pip \
	  && pip3 install ansible==${ANSIBLE_VERSION} \
    && echo "****** Remove unused system librabies ******" \
	  && apk del build-dependencies \
	  && rm -rf /var/cache/apk/*

# Install Citrix ADC Ansible modules
RUN wget -O /tmp/citrix-adc-ansible-modules.tar.gz https://github.com/citrix/citrix-adc-ansible-modules/archive/v1.8.tar.gz \
    && cd /tmp \
    && tar -zxvf citrix-adc-ansible-modules.tar.gz \
    && pip3 install citrix-adc-ansible-modules-1.8/deps/nitro-python-1.0_kamet.tar.gz \
    && python3 citrix-adc-ansible-modules-1.8/install.py \
    && rm -rf citrix-adc-ansible-modules-1.8 citrix-adc-ansible-modules.tar.gz \
    && mkdir /pwd

WORKDIR /pwd

CMD ["ansible-playbook", "--version"]
