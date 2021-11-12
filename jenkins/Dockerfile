FROM jenkins/jenkins:lts

USER root

COPY docker-ce-gpg-key /docker-ce-gpg-key
RUN cat /docker-ce-gpg-key | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
	"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian buster stable" \
	| tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
	    ca-certificates \
	    curl \
	    sudo \
	    gnupg2 \
	    software-properties-common \
	    docker-ce=5:20.10.8~3-0~debian-buster && \
		python3.9

RUN apt-get install -yq python3-pip

RUN ls

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archive/*.deb

# being lazy and making jenkins a sudoer so we dont need to futz w/ docker.sock permissions
RUN echo "jenkins:jenkins" | chpasswd && adduser jenkins sudo
RUN echo 'jenkins ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN mkdir /usr/share/jenkins/seed_jobs

USER jenkins

COPY plugins /usr/share/jenkins/plugins
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/plugins

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV JENKINS_USER admin
ENV JENKINS_PASS admin

COPY cfg-default-user.groovy /usr/share/jenkins/ref/init.groovy.d/
COPY cfg-disable-script-security.groovy /usr/share/jenkins/ref/init.groovy.d/

COPY builder/cfg_repo_builder.py /usr/share/jenkins
COPY builder/requirements.txt /usr/share/jenkins
COPY builder/requirements-dev.txt /usr/share/jenkins

COPY jobseed.yaml /usr/share/jenkins/seed_jobs/
# COPY jobinterfacedescr.groovy /usr/share/jenkins/seed_jobs/
# COPY jobpasswordrotate.groovy /usr/share/jenkins/seed_jobs/
COPY jobcfgrepo.groovy /usr/share/jenkins/seed_jobs/
ENV CASC_JENKINS_CONFIG /usr/share/jenkins/seed_jobs/jobseed.yaml
