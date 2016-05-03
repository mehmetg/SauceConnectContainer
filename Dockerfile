FROM ubuntu:latest
MAINTAINER Mehmet Gerceker <mehmetg@msn.com>
RUN ["mkdir", "sc_home"]
WORKDIR "sc_home"
COPY *.py "/sc_home"
RUN ["apt-get", "-qq", "update"]
RUN ["apt-get", "-y", "install", "curl", "wget", "python", "python-requests"]
RUN ["python", "sc_update.py"]
CMD ["python", "sc_update.py", "sc"]
WORKDIR "sc"
CMD ["ls"]
