# Usage Guide - Credential-License-Locator

Complete guide for using the Credential-License-Locator tool effectively.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [CLI Usage](#cli-usage)
4. [GUI Usage](#gui-usage)
5. [AI Configuration](#ai-configuration)
6. [Advanced Examples](#advanced-examples)
7. [Troubleshooting](#troubleshooting)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Grumpified-OGGVCT/Credential-License-Locator.git
cd Credential-License-Locator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys (Optional for AI features)
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Quick Start

### Test with Sample Data
```bash
# Scan the test data directory
python -m credlicense.cli scan test_data --scan-type all

# With AI analysis (requires API key)
python -m credlicense.cli scan test_data --ai --ai-provider ollama-cloud
```

## CLI Usage

### Basic Commands

#### View Help
```bash
python -m credlicense.cli --help
python -m credlicense.cli scan --help
```

#### Scan a Directory
```bash
# Basic scan (credentials and licenses)
python -m credlicense.cli scan /path/to/directory

# Save results to JSON
python -m credlicense.cli scan /path/to/directory --output results.json

# Scan only credentials
python -m credlicense.cli scan /path/to/directory --scan-type credentials

# Scan only licenses  
python -m credlicense.cli scan /path/to/directory --scan-type licenses
```

#### AI-Powered Analysis
```bash
# With Ollama CLOUD (default, requires OLLAMA_API_KEY)
python -m credlicense.cli scan /path/to/directory --ai

# With local Ollama (requires local Ollama server running)
python -m credlicense.cli scan /path/to/directory --ai --ai-provider ollama-local

# With OpenRouter (requires OPENROUTER_API_KEY)
python -m credlicense.cli scan /path/to/directory --ai --ai-provider openrouter
```

#### Generate Reports
```bash
# HTML report
python -m credlicense.cli report results.json --format html --output report.html

# Markdown report
python -m credlicense.cli report results.json --format markdown --output report.md
```

#### View Disclaimer
```bash
python -m credlicense.cli disclaimer
```

### Launch GUI
```bash
python -m credlicense.cli gui
```

## GUI Usage

### Starting the GUI
```bash
python -m credlicense.cli gui
# OR
python -m credlicense.ui.gui_app
```

### GUI Features
1. **Directory Selection**: Click "Browse..." to select a directory to scan
2. **Scan Type**: Choose All, Credentials Only, or Licenses Only
3. **AI Analysis**: Enable/disable and select provider (Ollama CLOUD, Local, or OpenRouter)
4. **Tabs**:
   - 📊 Summary: Overview of scan results
   - 🔐 Credentials: Detailed credential findings
   - 📜 Licenses: Detected licenses
   - 🤖 AI Analysis: AI-powered insights (if enabled)
5. **Export**: Save results in HTML, Markdown, or JSON format

## AI Configuration

### Ollama CLOUD (Recommended)
1. Get API key from https://ollama.ai/cloud
2. Set environment variable:
   ```bash
   export OLLAMA_API_KEY="your_api_key_here"
   ```
3. Use with:
   ```bash
   python -m credlicense.cli scan /path --ai --ai-provider ollama-cloud
   ```

### Ollama Local (Privacy Mode)
1. Install Ollama from https://ollama.ai
2. Start Ollama locally:
   ```bash
   ollama serve
   ```
3. Pull a model (optional):
   ```bash
   ollama pull llama2
   ```
4. Use with:
   ```bash
   python -m credlicense.cli scan /path --ai --ai-provider ollama-local
   ```

### OpenRouter
1. Get API key from https://openrouter.ai
2. Set environment variable:
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```
3. Use with:
   ```bash
   python -m credlicense.cli scan /path --ai --ai-provider openrouter
   ```

## Advanced Examples

### Example 1: Complete Security Audit Workflow
```bash
# 1. Scan your project with AI analysis
python -m credlicense.cli scan ~/my-project \
  --ai \
  --ai-provider ollama-cloud \
  --output audit-$(date +%Y%m%d).json

# 2. Generate HTML report
python -m credlicense.cli report audit-$(date +%Y%m%d).json \
  --format html \
  --output audit-report.html

# 3. Review the report
xdg-open audit-report.html  # Linux
# or
open audit-report.html      # macOS
```

### Example 2: License Compliance Check
```bash
# Scan only for licenses in your project
python -m credlicense.cli scan ~/my-project \
  --scan-type licenses \
  --output licenses.json

# Generate Markdown documentation
python -m credlicense.cli report licenses.json \
  --format markdown \
  --output LICENSES.md
```

### Example 3: Credential Security Audit
```bash
# Scan for credentials only
python -m credlicense.cli scan ~/my-project \
  --scan-type credentials \
  --ai \
  --output credentials-audit.json

# Review critical findings immediately
cat credentials-audit.json | jq '.credentials[] | select(.verified == true)'
```

### Example 4: Privacy-Focused Scan
```bash
# Use local Ollama for complete privacy (no data leaves your machine)
python -m credlicense.cli scan ~/sensitive-project \
  --ai \
  --ai-provider ollama-local \
  --output private-scan.json
```

### Example 5: Continuous Integration
```bash
#!/bin/bash
# Add to your CI pipeline

# Scan repository
python -m credlicense.cli scan . \
  --scan-type credentials \
  --output ci-scan.json

# Check for verified credentials
VERIFIED=$(cat ci-scan.json | jq '.credentials[] | select(.verified == true)' | wc -l)

if [ $VERIFIED -gt 0 ]; then
  echo "ERROR: Found $VERIFIED verified credentials!"
  exit 1
fi

echo "No verified credentials found. Build continues."
```

## Troubleshooting

### TruffleHog Not Found
```bash
# TruffleHog is the external binary, not truffleHog3
# Install it from: https://github.com/trufflesecurity/trufflehog
# For now, the scanner will continue without it
```

### AI Analysis Fails
```bash
# Check your API key is set
echo $OLLAMA_API_KEY
echo $OPENROUTER_API_KEY

# For local Ollama, check it's running
curl http://localhost:11434/api/tags

# Test with a simple scan first
python -m credlicense.cli scan test_data --ai
```

### Permission Denied Errors
```bash
# Make sure you have read permissions on the directory
ls -la /path/to/directory

# Run with appropriate permissions
sudo python -m credlicense.cli scan /protected/directory
```

### GUI Doesn't Launch
```bash
# Tkinter might not be installed
sudo apt-get install python3-tk  # Debian/Ubuntu
sudo yum install python3-tkinter  # RHEL/CentOS

# Test Tkinter
python3 -m tkinter
```

### Dependency Conflicts
```bash
# Use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Best Practices

### 1. Regular Scanning
- Run scans regularly (weekly or before releases)
- Integrate into CI/CD pipelines
- Document all findings

### 2. Immediate Response to Findings
- Rotate verified credentials immediately
- Review access logs
- Remove from version control history

### 3. Prevention
- Use pre-commit hooks
- Enable secret scanning in repositories
- Train team on secure coding practices

### 4. Documentation
- Keep scan reports for compliance
- Document license usage
- Maintain credential inventory

## Support and Resources

- **Documentation**: [GitHub README](https://github.com/Grumpified-OGGVCT/Credential-License-Locator)
- **Issues**: [GitHub Issues](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/discussions)

## Legal Notice

This tool is for authorized security auditing only. Users are responsible for ensuring compliance with all applicable laws and regulations. Only scan systems you own or have explicit permission to scan.
