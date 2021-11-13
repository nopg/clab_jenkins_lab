FROM python:3.9.6-buster

RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

ENV SERVICE_PASS "service"

#COPY common.py /

ENTRYPOINT ["python"]
#CMD ["cfg_repo_builder.py"]
