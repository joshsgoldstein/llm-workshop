# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    apt-transport-https \
    gnupg2

# Install Python dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install notebook ipykernel

# Install kubectl
RUN curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y kubectl

# Install Helm
RUN curl https://baltocdn.com/helm/signing.asc | apt-key add - \
    && echo "deb https://baltocdn.com/helm/stable/debian/ all main" > /etc/apt/sources.list.d/helm-stable-debian.list \
    && apt-get update \
    && apt-get install -y helm

# Add the Python kernel to Jupyter
RUN python -m ipykernel install --user --name python-kernel

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose port for Jupyter Notebook
EXPOSE 8888

# Set the default command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
