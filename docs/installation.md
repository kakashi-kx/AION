# 🔧 AION Installation Guide

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Kali, Ubuntu, Parrot), macOS, or WSL2 on Windows
- **Python**: 3.9 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 10GB free space
- **Internet**: Required for initial setup and model downloads

### Quick Installation

## 🚀 Method 1: Automatic Installation

```bash
# Clone the repository
git clone https://github.com/kakashi-kx/AION.git
cd AION

# Make install script executable
chmod +x scripts/install.sh

# Run installation
./scripts/install.sh
```
🐍 Method 2: Manual Installation
Step 1: Install Python Dependencies
bash

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install AION in development mode
pip install -e .

Step 2: Install Ollama (for Local AI)
bash

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# Download from https://ollama.com/download/windows

# Start Ollama service
ollama serve &

Step 3: Download AI Models
bash

# Pull recommended models
ollama pull llama3      # General purpose
ollama pull mistral     # Fast inference
ollama pull phi3        # Lightweight
ollama pull nomic-embed-text  # For embeddings

# Optional: Pull specialized models
ollama pull codellama   # Code analysis
ollama pull neural-chat # Conversation
ollama pull dolphin-mistral  # Uncensored (use carefully)

Step 4: Verify Installation
bash

# Run tests
pytest tests/

# Check installation
python -c "from core import AIOrchestrator; print('✅ AION installed successfully!')"

🐳 Method 3: Docker Installation
bash

# Build Docker image
docker build -t aion:latest .

# Run container
docker run -it --gpus all -v $(pwd)/data:/app/data aion:latest

# Or use docker-compose
docker-compose up -d

