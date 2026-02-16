# 1. Use an official Python runtime as a parent image
FROM python:3.14-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container
# We do this first so Docker can cache the installed libraries
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# When you run pip install normally on your computer, Python saves a copy of every library you download in a "cache" folder. 
# This is great for your PC because if you ever need to reinstall that library, pip doesn't have to download it from the internet again.
# However, in the world of Docker, that cache is just dead weight. 
# When you build a Docker image, it creates a snapshot of everything in the container at that moment. 
# If you have a cache folder with all those libraries, it will include that in the image, making it unnecessarily large.

# 5. Copy the rest of your application code
COPY . .

# 6. Run the bot
CMD ["python", "main.py"]

