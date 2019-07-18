
# use the ubuntu latest image
FROM ubuntu:16.04

# Update and upgrade system
RUN apt-get -qq update && apt-get -qq --yes upgrade

# install sys utils
RUN apt-get -qq install --yes build-essential libevent-dev libssl-dev curl g++ python

# install tor
ENV TOR_VERSION 0.2.9.13
RUN curl -0 -L https://www.torproject.org/dist/tor-${TOR_VERSION}.tar.gz | tar xz -C /tmp
RUN cd /tmp/tor-${TOR_VERSION} && ./configure
RUN cd /tmp/tor-${TOR_VERSION} && make -j 4
RUN cd /tmp/tor-${TOR_VERSION} && make install

# install delegate
ENV DELEGATE_VERSION 9.9.13
RUN curl ftp://anonymous@ftp.delegate.org/pub/DeleGate/delegate${DELEGATE_VERSION}.tar.gz | tar xz -C /tmp
RUN echo "ADMIN=root@root.com" > /tmp/delegate${DELEGATE_VERSION}/src/DELEGATE_CONF
RUN sed -i -e '1i#include <util.h>\' /tmp/delegate${DELEGATE_VERSION}/maker/_-forkpty.c
RUN cd /tmp/delegate${DELEGATE_VERSION} && make

# install haproxy
ENV HAPROXY_VERSION 1.6.8
RUN curl -0 -L http://haproxy.1wt.eu/download/1.6/src/haproxy-${HAPROXY_VERSION}.tar.gz | tar xz -C /tmp
RUN cd /tmp/haproxy-${HAPROXY_VERSION}/ && make TARGET=linux2628 USE_OPENSSL=1 USE_ZLIB=1
RUN cd /tmp/haproxy-${HAPROXY_VERSION}/ && make install

ENV NODES=10

ADD entry.sh /
RUN chmod +x /entry.sh
RUN sed -i 's/\r$//' entry.sh

RUN mkdir -p /usr/local/etc/tor
# RUN echo 'MaxCircuitDirtiness 10' >> /usr/local/etc/tor/torrc
RUN echo "ExitNodes {ua},{uk},{lv},{lt},{fi},{se},{no},{pl},{de},{fr},{nl},{be},{cz},{at} StrictNodes 1"  >> /usr/local/etc/tor/torrc
RUN echo "EntryNodes {ua},{uk},{lv},{lt},{fi},{se},{no},{pl},{de},{fr},{nl},{be},{cz},{at} StrictNodes 1"  >> /usr/local/etc/tor/torrc


ADD generate.py /

CMD ["/entry.sh"]
