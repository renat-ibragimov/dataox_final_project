FROM python:3.10
WORKDIR /dataox_final_project
COPY . ./dataox_final_project
COPY requirements.txt /dataox_final_project/

RUN python -m venv /opt/venv
RUN pip install --upgrade pip
RUN pip install --requirement /dataox_final_project/requirements.txt
