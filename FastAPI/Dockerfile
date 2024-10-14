# base image 
FROM python:3.12 as development

# set environment variables  
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Working directory 
WORKDIR /FastAPI

# install dependencies  
RUN pip install --upgrade pip 

COPY ./ ./
# run this command to install all dependencies  
RUN pip install -r requirements.txt

# port where the FastAPI app runs  
EXPOSE 8000  

CMD ["python3", "api.py"]