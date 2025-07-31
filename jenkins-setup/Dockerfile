# jenkins-setup/docker-compose/Dockerfile

FROM jenkins/jenkins:lts

USER root

# Install required tools: Docker CLI + Python 3.11 + pip + curl
RUN apt-get update && \
    apt-get install -y docker.io python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to docker group to allow socket access
ARG DOCKER_GID=0
RUN groupadd -g ${DOCKER_GID} docker || true && usermod -aG docker jenkins


# Add plugin install CLI
RUN curl -fsSL https://github.com/jenkinsci/plugin-installation-manager-tool/releases/latest/download/jenkins-plugin-manager-2.13.2.jar -o /usr/share/jenkins/ref/jenkins-plugin-manager.jar

COPY ./jenkins/plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install plugins before starting Jenkins
RUN java -jar /usr/share/jenkins/ref/jenkins-plugin-manager.jar \
    --war /usr/share/jenkins/jenkins.war \
    --plugin-file /usr/share/jenkins/ref/plugins.txt \
    --plugin-download-directory /usr/share/jenkins/ref/plugins

USER jenkins
