FROM debian:buster
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates=20200601~deb10u2
RUN echo "deb [trusted=yes] https://apt.fury.io/netdevops/ /" | \
    tee -a /etc/apt/sources.list.d/netdevops.list
RUN apt-get update && \
    apt-get -yq --no-install-recommends install \
        containerlab=0.16.2 \
        python3.7=3.7.3-2+deb10u3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archive/*.deb
COPY launcher.py /

#ENTRYPOINT ["./launcher.py"]