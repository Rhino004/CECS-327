FROM python:3.9-slim
WORKDIR /Project_3_p2p
COPY . .
RUN pip install flask
EXPOSE 5000
CMD ["python", "bootstrap.py"]