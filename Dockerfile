FROM ubuntu:latest
MAINTAINER Mehmet Gerceker <mehmetg@msn.com>
RUN ["mkdir", "/sc_home"]
COPY *.py "/sc_home"
WORKDIR "/sc_home"
RUN ["apt-get", "-qq", "update"]
RUN ["apt-get", "-y", "install", "curl", "wget", "python", "python-requests"]
RUN ["python", "sc_update.py"]
CMD ["echo Updating Sauce Connect"]
CMD ["python", "sc_update.py"]
CMD ["source", "sc.sh"]