FROM jetbrains/teamcity-agent:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir flake8 bandit

RUN groupadd -g 999 docker || true
RUN usermod -aG docker buildagent
