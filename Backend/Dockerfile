# base image 
FROM python:3.12 AS development

# set environment variables  
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYDEVD_DISABLE_FILE_VALIDATION 1
# ENV -Xfrozen_modules=off

# allow remote debugging
# ENV DEBUG=True

# install dependencies  
# RUN apt-get update && apt-get upgrade -y && apt-get clean

# Working directory 
WORKDIR /Backend

# install dependencies  
RUN pip install --upgrade pip 

COPY ./ ./
# run this command to install all dependencies  
RUN pip install -r requirements.txt

# Install debugpy for remote debugging
RUN pip install debugpy

# port where the FastAPI app runs  
EXPOSE 8000  
# Expose debug port (default for debugpy is 5678)
EXPOSE 5678

CMD ["uvicorn", "--reload", "api:app", "--host", "0.0.0.0", "--port", "8000"]