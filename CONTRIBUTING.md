# Contributing to Credential-License-Locator

Thank you for considering contributing to Credential-License-Locator! This document provides guidelines and instructions for contributing.

## Code of Conduct

### Our Pledge
- Be respectful and inclusive
- Focus on what is best for the community
- Show empathy towards others
- Use welcoming and inclusive language

### Our Standards
- ✅ Constructive feedback
- ✅ Accepting responsibility for mistakes
- ✅ Focusing on security and privacy
- ❌ Trolling or insulting comments
- ❌ Public or private harassment
- ❌ Publishing others' private information

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version)
   - Sample data (if applicable)

### Suggesting Features
1. Check if the feature has been requested
2. Explain the use case
3. Describe the proposed solution
4. Consider implementation complexity

### Code Contributions

#### Getting Started
```bash
# Fork the repository
git clone https://github.com/YOUR-USERNAME/Credential-License-Locator.git
cd Credential-License-Locator

# Create a branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Test your changes
python -m credlicense.cli scan test_data

# Commit and push
git add .
git commit -m "Add feature: description"
git push origin feature/your-feature-name

# Create a Pull Request
```

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add comments for complex logic

#### Example
```python
def scan_directory(self, directory: str) -> List[Dict[str, Any]]:
    """
    Scan a directory for licenses.
    
    Args:
        directory: Path to the directory to scan
        
    Returns:
        List of license findings with details
        
    Raises:
        ValueError: If directory doesn't exist
    """
    # Implementation
    pass
```

### Testing
- Test all new features
- Ensure existing functionality still works
- Test with the test_data directory
- Test both CLI and GUI interfaces

### Documentation
- Update README.md if needed
- Update USAGE.md for new features
- Add docstrings to new code
- Update type hints

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Text editor or IDE

### Installation
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Credential-License-Locator.git
cd Credential-License-Locator

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests
```bash
# Test CLI
python -m credlicense.cli scan test_data

# Test with different scan types
python -m credlicense.cli scan test_data --scan-type credentials
python -m credlicense.cli scan test_data --scan-type licenses

# Test GUI (if you have display)
python -m credlicense.cli gui
```

## Areas for Contribution

### High Priority
- [ ] Additional credential detectors
- [ ] More license pattern recognition
- [ ] Performance optimizations
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation improvements

### Medium Priority
- [ ] Additional report formats (PDF, CSV)
- [ ] Configuration file support
- [ ] Custom scanning rules
- [ ] Exclude patterns
- [ ] Additional AI providers

### Nice to Have
- [ ] Web interface
- [ ] REST API
- [ ] Plugin system
- [ ] Language-specific scanners
- [ ] Database for tracking findings over time

## Pull Request Process

1. **Update Documentation**: Ensure README, USAGE, or other docs are updated
2. **Test Thoroughly**: Test your changes with various scenarios
3. **Follow Code Style**: Maintain consistent code style
4. **Write Clear Commits**: Use descriptive commit messages
5. **One Feature Per PR**: Keep pull requests focused
6. **Respond to Feedback**: Address review comments promptly

### PR Template
```markdown
## Description
[Describe what this PR does]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
[Describe how you tested this]

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings
- [ ] PR description is clear
```

## Security Considerations

### Security Vulnerabilities
- Report security issues privately via GitHub Security Advisories
- Do not open public issues for security vulnerabilities
- Allow time for fixes before public disclosure

### Credential Handling
- Never commit real credentials
- Use fake/example credentials in tests
- Redact sensitive information in logs
- Follow secure coding practices

### Privacy
- Respect user privacy
- Minimize data collection
- Provide opt-out options
- Document data handling

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open a [Discussion](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/discussions)
- Check existing [Issues](https://github.com/Grumpified-OGGVCT/Credential-License-Locator/issues)
- Review [Documentation](README.md)

## Thank You!

Your contributions help make this tool better for everyone. Whether it's code, documentation, bug reports, or feature suggestions, all contributions are valued and appreciated!

---

**Remember**: This tool is for ethical security auditing only. All contributions must align with this mission.
