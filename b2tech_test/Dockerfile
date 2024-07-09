# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /usr/src/app/

# gunicorn 설치
RUN pip install gunicorn

RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8888

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "b2tech_test.wsgi:application"]
