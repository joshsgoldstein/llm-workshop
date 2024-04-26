FROM python:3.10.14-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y curl git apt-transport-https gnupg2

# Install Python dependencies including Jupyter
# Ensure you have a requirements.txt in your context if you uncomment the following lines
# COPY requirements.txt /workspace/
# RUN pip install --no-cache-dir -r requirements.txt

# Install Jupyter and ipykernel
RUN pip install notebook ipykernel

# Install kubectl
RUN apt-get install -y apt-transport-https gnupg2 curl && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y kubectl

# Setup the Kubernetes config
ARG KUBECONFIG_DATA
RUN mkdir -p /root/.kube && echo "${KUBECONFIG_DATA}" | base64 --decode > /root/.kube/config

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
