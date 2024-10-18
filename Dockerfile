FROM python:3.10

# Set up the working directory
WORKDIR /app

EXPOSE 8007
# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application to the container
COPY . .

# Run the application
CMD ["python", "manage.py", "runserver"]