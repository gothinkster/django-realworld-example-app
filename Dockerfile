FROM python:3

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.0.0.1744-linux.zip && \
    unzip sonar-scanner-cli-4.0.0.1744-linux.zip && \
    rm sonar-scanner-4.0.0.1744-linux/conf/sonar-scanner.properties && \
    apt-get update && \
    apt-get install openjdk-8-jre-headless && \
    rm -rf /var/lib/apt/lists/*

COPY sonar-scanner.properties sonar-scanner-4.0.0.1744-linux/conf/sonar-scanner.properties