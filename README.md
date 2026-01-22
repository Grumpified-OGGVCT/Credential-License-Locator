# Credential-License-Locator

A comprehensive privacy-focused tool to scan local directories for stored software licenses and credentials. Features advanced AI-powered analysis through cloud and local AI models.

## ⚠️ Ethical Use Warning

**This tool is designed for legitimate security auditing and credential management on systems you own or have explicit permission to scan.**

### Acceptable Uses
- ✅ Scanning your own systems and files
- ✅ Security auditing with proper authorization
- ✅ Organizing your personal credentials and licenses
- ✅ Compliance checking for your projects

### Prohibited Uses
- ❌ Unauthorized access to others' systems
- ❌ Scanning systems without permission
- ❌ Any illegal or unethical activities
- ❌ Violating terms of service

## Features

### 🔍 Comprehensive Scanning
- **Credential Detection**: Integrates TruffleHog for finding API keys, passwords, tokens, and other secrets
- **License Scanning**: Detects software licenses in files, headers, and dependencies
- **Multi-format Support**: Scans Python, JavaScript, Java, C++, Go, Rust, and more

### 🤖 AI-Powered Analysis
Three AI provider options:
1. **Ollama CLOUD** (Primary) - Full cloud API with advanced capabilities
2. **Ollama Local** (Privacy Mode) - Simple local server for privacy-conscious users
3. **OpenRouter** (Alternative) - Access to multiple AI models

### 🎨 Dual Interface
- **CLI**: Rich command-line interface with colored output and progress indicators
- **GUI**: Modern graphical interface with tabbed results and export options

### 📊 Reporting
- HTML reports with styling and statistics
- Markdown reports for documentation
- JSON exports for programmatic access
- Real-time result categorization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- TruffleHog (installed automatically)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Grumpified-OGGVCT/Credential-License-Locator.git
cd Credential-License-Locator

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Configuration

### API Keys Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:

```bash
# For Ollama CLOUD (recommended)
OLLAMA_API_KEY=your_ollama_cloud_api_key

# For OpenRouter (alternative)
OPENROUTER_API_KEY=your_openrouter_api_key

# For local Ollama (optional)
OLLAMA_LOCAL_URL=http://localhost:11434
```

### Getting API Keys

- **Ollama CLOUD**: Visit https://ollama.ai/cloud to sign up
- **OpenRouter**: Visit https://openrouter.ai to get an API key
- **Local Ollama**: Install from https://ollama.ai and run locally

## Usage

### Command Line Interface (CLI)

#### Basic Scan
```bash
# Scan a directory for credentials and licenses
credlicense scan /path/to/directory

# Scan with AI analysis (Ollama CLOUD)
credlicense scan /path/to/directory --ai

# Use specific AI provider
credlicense scan /path/to/directory --ai --ai-provider ollama-cloud
credlicense scan /path/to/directory --ai --ai-provider ollama-local
credlicense scan /path/to/directory --ai --ai-provider openrouter

# Scan only for credentials
credlicense scan /path/to/directory --scan-type credentials

# Scan only for licenses
credlicense scan /path/to/directory --scan-type licenses

# Save results to JSON
credlicense scan /path/to/directory --output results.json
```

#### Generate Reports
```bash
# Generate HTML report from scan results
credlicense report results.json --format html --output report.html

# Generate Markdown report
credlicense report results.json --format markdown --output report.md
```

#### View Disclaimer
```bash
credlicense disclaimer
```

### Graphical User Interface (GUI)

Launch the GUI:
```bash
credlicense gui
```

Or run directly:
```bash
python -m credlicense.ui.gui_app
```

### Using as a Python Library

```python
from credlicense.core.credential_scanner import CredentialScanner
from credlicense.core.license_scanner import LicenseScanner
from credlicense.ai.assistant import AIAssistant

# Scan for credentials
cred_scanner = CredentialScanner()
credentials = cred_scanner.scan_directory("/path/to/directory")

# Scan for licenses
lic_scanner = LicenseScanner()
licenses = lic_scanner.scan_directory("/path/to/directory")

# AI analysis with Ollama CLOUD
ai = AIAssistant(provider="ollama-cloud")
analysis = ai.analyze_findings(credentials, licenses)

# AI analysis with local Ollama (privacy mode)
ai_local = AIAssistant(provider="ollama-local")
analysis_local = ai_local.analyze_findings(credentials, licenses)

# Get remediation advice
for finding in credentials:
    advice = ai.get_remediation_advice(finding)
    print(advice)
```

## AI Provider Comparison

### Ollama CLOUD (Recommended)
- ✅ Full cloud API with advanced capabilities
- ✅ Fast and reliable
- ✅ No local setup required
- ✅ Access to latest models
- 🔑 Requires API key (OLLAMA_API_KEY)

### Ollama Local (Privacy Mode)
- ✅ Complete data privacy
- ✅ No API costs
- ✅ Works offline
- ⚙️ Requires local Ollama installation
- 🐌 May be slower than cloud

### OpenRouter
- ✅ Access to multiple AI models
- ✅ Flexible pricing
- ✅ Good for experimentation
- 🔑 Requires API key (OPENROUTER_API_KEY)

## Examples

### Example 1: Quick Security Audit
```bash
# Scan your project directory with AI analysis
credlicense scan ~/my-project --ai --output security-audit.json

# Generate a detailed HTML report
credlicense report security-audit.json --format html --output audit-report.html
```

### Example 2: License Compliance Check
```bash
# Scan only for licenses
credlicense scan ~/my-project --scan-type licenses --output licenses.json

# Review in markdown format
credlicense report licenses.json --format markdown --output licenses.md
```

### Example 3: Privacy-Focused Scan
```bash
# Use local Ollama for complete privacy
credlicense scan ~/sensitive-project --ai --ai-provider ollama-local
```

## Security Best Practices

### If Credentials Are Found:

1. **Immediate Action Required**
   - Rotate/revoke ALL exposed credentials immediately
   - Review access logs for unauthorized usage
   - Check if credentials were committed to version control

2. **Remove from Files**
   - Delete credentials from all files
   - Use `git filter-branch` or BFG Repo-Cleaner for git history
   - Update `.gitignore` to prevent future commits

3. **Implement Proper Secret Management**
   - Use environment variables
   - Implement HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault
   - Use encrypted configuration files
   - Enable secret scanning in CI/CD

4. **Monitor and Prevent**
   - Set up automated secret scanning
   - Use pre-commit hooks
   - Regular security audits
   - Team security training

## Project Structure

```
Credential-License-Locator/
├── credlicense/
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── core/
│   │   ├── credential_scanner.py  # Credential detection
│   │   └── license_scanner.py     # License detection
│   ├── ui/
│   │   └── gui_app.py         # Graphical interface
│   ├── ai/
│   │   └── assistant.py       # AI integration (cloud & local)
│   └── utils/
│       ├── disclaimer.py      # Ethical warnings
│       └── report_generator.py # Report generation
├── requirements.txt
├── setup.py
├── .env.example
└── README.md
```

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/Grumpified-OGGVCT/Credential-License-Locator)
- 🐛 [Issue Tracker](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/issues)
- 💬 [Discussions](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/discussions)

## Disclaimer

This tool is provided "as is" for legitimate security and compliance purposes. Users are solely responsible for ensuring their use complies with all applicable laws, regulations, and ethical standards. Unauthorized access to computer systems is illegal.

**Use responsibly. Only scan systems you own or have explicit permission to scan.**

---

Made with ❤️ for security-conscious developers

