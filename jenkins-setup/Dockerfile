# jenkins-setup/docker-compose/Dockerfile

FROM jenkins/jenkins:lts

USER root

# Add plugin install CLI
RUN curl -fsSL https://github.com/jenkinsci/plugin-installation-manager-tool/releases/latest/download/jenkins-plugin-manager-2.13.2.jar -o /usr/share/jenkins/ref/jenkins-plugin-manager.jar

COPY ./jenkins/plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install plugins before starting Jenkins
RUN java -jar /usr/share/jenkins/ref/jenkins-plugin-manager.jar \
    --war /usr/share/jenkins/jenkins.war \
    --plugin-file /usr/share/jenkins/ref/plugins.txt \
    --plugin-download-directory /usr/share/jenkins/ref/plugins

USER jenkins
