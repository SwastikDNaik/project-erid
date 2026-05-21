#!/bin/bash

# Start Ollama
ollama serve &

# Wait for server
sleep 10

# Pull model
ollama pull phi3

# Start streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0