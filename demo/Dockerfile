FROM python:3.9.6-buster

COPY requirements.txt /

RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

ENV SERVICE_PASS "service"

COPY common.py /

ENTRYPOINT ["python"]
CMD ["build_configs.py"]
