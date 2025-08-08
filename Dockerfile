# Use Fedora as base image
FROM fedora:latest

# Install Python and pip
RUN microdnf update -y && \
    microdnf install -y python3 python3-pip && \
    microdnf clean all

# Install uv
RUN pip install uv

# Create app directory
WORKDIR /app

# Copy the entrypoint script
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Expose default port (will be overridden by env var)
EXPOSE 9000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the entrypoint
ENTRYPOINT ["./entrypoint.sh"] 