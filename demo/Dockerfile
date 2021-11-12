FROM python:3.9.6-buster

COPY requirements.txt /
COPY requirements-dev.txt /
COPY cfg_repo_builder.py /

RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

ENV SERVICE_PASS "service"

#COPY common.py /

ENTRYPOINT ["python"]
CMD ["cfg_repo_builder.py"]
