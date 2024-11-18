# Use the official Python image from Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire content of your app into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "demo_churn.py"]
