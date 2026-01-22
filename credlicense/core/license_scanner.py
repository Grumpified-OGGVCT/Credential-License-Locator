#!/usr/bin/env python3
"""
License Scanner Module

This module scans for software licenses in files and dependencies.
"""

import os
import subprocess
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
import re

# Set up logging for debugging
logger = logging.getLogger(__name__)


class LicenseScanner:
    """Scanner for detecting software licenses."""
    
    # Common license patterns
    LICENSE_PATTERNS = {
        "MIT": r"MIT License|Permission is hereby granted, free of charge",
        "Apache-2.0": r"Apache License, Version 2\.0",
        "GPL-3.0": r"GNU GENERAL PUBLIC LICENSE\s+Version 3",
        "GPL-2.0": r"GNU GENERAL PUBLIC LICENSE\s+Version 2",
        "BSD-3-Clause": r"BSD 3-Clause License|Redistribution and use in source and binary forms",
        "ISC": r"ISC License|Permission to use, copy, modify",
        "LGPL": r"GNU Lesser General Public License",
        "MPL-2.0": r"Mozilla Public License Version 2\.0",
        "AGPL-3.0": r"GNU AFFERO GENERAL PUBLIC LICENSE\s+Version 3",
    }
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
    
    def scan_directory(self, directory: str) -> List[Dict[str, Any]]:
        """
        Scan a directory for license files and information.
        
        Args:
            directory: Path to the directory to scan
            
        Returns:
            List of license findings
        """
        self.results = []
        directory_path = Path(directory).resolve()
        
        if not directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        # Find license files
        self._scan_license_files(directory_path)
        
        # Scan for license headers in source files
        self._scan_source_files(directory_path)
        
        # Scan Python package licenses if applicable
        self._scan_python_packages(directory_path)
        
        return self.results
    
    def _scan_license_files(self, directory_path: Path):
        """Scan for explicit license files."""
        license_filenames = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYRIGHT"]
        
        for root, dirs, files in os.walk(directory_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
            
            for filename in files:
                if filename.upper() in [f.upper() for f in license_filenames]:
                    filepath = Path(root) / filename
                    license_type = self._identify_license(filepath)
                    
                    self.results.append({
                        "type": "license_file",
                        "file": str(filepath),
                        "license": license_type,
                        "confidence": "HIGH" if license_type != "Unknown" else "LOW"
                    })
    
    def _scan_source_files(self, directory_path: Path):
        """Scan source files for license headers."""
        source_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.ts']
        
        for root, dirs, files in os.walk(directory_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
            
            for filename in files:
                if any(filename.endswith(ext) for ext in source_extensions):
                    filepath = Path(root) / filename
                    
                    try:
                        # Read first 50 lines to check for license headers
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            header = ''.join(f.readlines()[:50])
                            
                        license_type = self._identify_license_from_text(header)
                        if license_type != "Unknown":
                            self.results.append({
                                "type": "license_header",
                                "file": str(filepath),
                                "license": license_type,
                                "confidence": "MEDIUM"
                            })
                    except Exception:
                        continue
    
    def _scan_python_packages(self, directory_path: Path):
        """Scan Python package dependencies for licenses."""
        # Check if this is a Python project
        has_requirements = (directory_path / "requirements.txt").exists()
        has_setup_py = (directory_path / "setup.py").exists()
        has_pyproject = (directory_path / "pyproject.toml").exists()
        
        if has_requirements or has_setup_py or has_pyproject:
            try:
                # Check if pip-licenses is available
                check_cmd = ["pip-licenses", "--help"]
                subprocess.run(check_cmd, capture_output=True, timeout=5, check=True)
                
                # Run pip-licenses
                result = subprocess.run(
                    ["pip-licenses", "--format=json"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(directory_path)
                )
                
                if result.returncode == 0 and result.stdout:
                    packages = json.loads(result.stdout)
                    for package in packages:
                        self.results.append({
                            "type": "package_license",
                            "package": package.get("Name", "Unknown"),
                            "version": package.get("Version", "Unknown"),
                            "license": package.get("License", "Unknown"),
                            "confidence": "HIGH"
                        })
            except FileNotFoundError:
                # pip-licenses not installed, skip package scanning
                logger.debug("pip-licenses not installed, skipping package license scanning")
            except subprocess.TimeoutExpired:
                logger.debug("pip-licenses timed out")
            except subprocess.CalledProcessError as e:
                logger.debug(f"pip-licenses command failed: {e}")
            except json.JSONDecodeError as e:
                logger.debug(f"Failed to parse pip-licenses output: {e}")
    
    def _identify_license(self, filepath: Path) -> str:
        """Identify license type from a license file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return self._identify_license_from_text(content)
        except Exception:
            return "Unknown"
    
    def _identify_license_from_text(self, text: str) -> str:
        """Identify license type from text content."""
        for license_name, pattern in self.LICENSE_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return license_name
        return "Unknown"
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of license scan results."""
        license_types = {}
        for result in self.results:
            license_name = result.get("license", "Unknown")
            license_types[license_name] = license_types.get(license_name, 0) + 1
        
        return {
            "total_findings": len(self.results),
            "license_files": sum(1 for r in self.results if r.get("type") == "license_file"),
            "license_headers": sum(1 for r in self.results if r.get("type") == "license_header"),
            "package_licenses": sum(1 for r in self.results if r.get("type") == "package_license"),
            "license_types": license_types
        }
