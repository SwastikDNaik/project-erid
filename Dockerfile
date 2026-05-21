FROM ubuntu:22.04

# System packages
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Start script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]