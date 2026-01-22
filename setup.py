#!/usr/bin/env python3
"""Setup script for Credential-License-Locator."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="credential-license-locator",
    version="1.0.0",
    author="Grumpified-OGGVCT",
    description="A privacy-focused tool to scan local drives for stored software licenses and credentials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Grumpified-OGGVCT/Credential-License-Locator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "truffleHog3>=3.0.0",
        "gitpython>=3.1.0",
        "licensecheck>=2024.1",
        "piplicenses>=4.3.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "requests>=2.31.0",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "credlicense=credlicense.cli:main",
        ],
    },
)
