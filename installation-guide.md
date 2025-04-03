# Installation Guide - LLM Prompt Engineering Framework

This guide provides detailed instructions for installing and setting up the LLM Prompt Engineering Framework.

## System Requirements

- Python 3.8 or higher
- 2GB of RAM (4GB recommended)
- Internet connection for API access

## Installation Methods

Choose one of the following installation methods:

### Method 1: Simple Installation (Recommended for Most Users)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/prompt-engineering-framework.git
   cd prompt-engineering-framework
   ```

2. **Run the setup script**:
   ```bash
   python run.py --setup-only
   ```

3. **Start the application**:
   ```bash
   python run.py
   ```

### Method 2: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/prompt-engineering-framework.git
   cd prompt-engineering-framework
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**:
   ```bash
   mkdir -p templates stored_states
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred text editor to add API keys
   ```

6. **Run the application**:
   ```bash
   streamlit run app.py
   ```

### Method 3: Docker Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/prompt-engineering-framework.git
   cd prompt-engineering-framework
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred text editor to add API keys
   ```

3. **Build and start with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

## API Keys Setup

### Getting API Keys

To use LLM API integration, you'll need API keys from providers:

1. **Anthropic Claude API Key**:
   - Sign up at [Anthropic](https://www.anthropic.com/)
   - Navigate to the API section to create an API key

2. **OpenAI API Key** (optional):
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Go to API keys section to create a new secret key

### Configuring API Keys

There are multiple ways to configure your API keys:

1. **Environment variables in `.env` file**:
   ```
   ANTHROPIC_API_KEY=sk-ant-api...
   OPENAI_API_KEY=sk-...
   ```

2. **Through the UI**:
   - Toggle "Use LLM API" in the content generation section
   - Enter your API key in the settings panel that appears

3. **Using the API Key Manager**:
   - Run the application in development mode: `python run.py --dev`
   - In the sidebar, open the "API Key Management" section

## Troubleshooting

### Common Issues

1. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission errors when creating directories**:
   ```bash
   # Run with admin privileges or adjust permissions
   sudo mkdir -p templates stored_states
   sudo chown -R $USER:$USER templates stored_states
   ```

3. **Port already in use**:
   ```bash
   # Run on a different port
   python run.py --port 8502
   ```

4. **API connection errors**:
   - Check your internet connection
   - Verify your API keys are correct
   - Check provider service status

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/yourusername/prompt-engineering-framework/issues) for similar problems
2. Create a new issue with details about your problem
3. Include your system information and error messages

## Next Steps

After installation, check out the [README.md](README.md) for usage instructions and the [README_TESTING.md](README_TESTING.md) for testing information.

Happy prompt engineering!