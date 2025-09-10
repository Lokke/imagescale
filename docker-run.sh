# Build the Docker image
docker build -t imagescale .

# Run the container on port 8724
docker run -p 8724:8724 imagescale

# Access the application at:
# http://localhost:8724
