#!/usr/bin/env python3
"""
Credential Scanner Module

This module integrates TruffleHog for detecting credentials in files and repositories.
"""

import os
import subprocess
import json
from typing import List, Dict, Any
from pathlib import Path


class CredentialScanner:
    """Scanner for detecting credentials using TruffleHog."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
    
    def scan_directory(self, directory: str) -> List[Dict[str, Any]]:
        """
        Scan a directory for credentials using TruffleHog.
        
        Args:
            directory: Path to the directory to scan
            
        Returns:
            List of findings with details
        """
        self.results = []
        directory_path = Path(directory).resolve()
        
        if not directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
        
        # Use TruffleHog to scan the filesystem
        try:
            # TruffleHog filesystem scan
            cmd = [
                "trufflehog",
                "filesystem",
                str(directory_path),
                "--json"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.stdout:
                # Parse JSON output line by line
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            finding = json.loads(line)
                            self.results.append(self._format_finding(finding))
                        except json.JSONDecodeError:
                            continue
            
        except subprocess.TimeoutExpired:
            print("Warning: TruffleHog scan timed out")
        except FileNotFoundError:
            print("Warning: TruffleHog not installed. Install with: pip install truffleHog3")
        except Exception as e:
            print(f"Error running TruffleHog: {e}")
        
        return self.results
    
    def _format_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Format TruffleHog finding into standardized format."""
        return {
            "type": "credential",
            "detector": finding.get("DetectorName", "Unknown"),
            "file": finding.get("SourceMetadata", {}).get("Data", {}).get("Filesystem", {}).get("file", "Unknown"),
            "line": finding.get("SourceMetadata", {}).get("Data", {}).get("Filesystem", {}).get("line", 0),
            "secret": finding.get("Raw", "***REDACTED***")[:50] + "...",  # Truncate for safety
            "verified": finding.get("Verified", False),
            "severity": "HIGH" if finding.get("Verified", False) else "MEDIUM",
            "raw_data": finding
        }
    
    def scan_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Scan a single file for credentials.
        
        Args:
            filepath: Path to the file to scan
            
        Returns:
            List of findings
        """
        file_path = Path(filepath).resolve()
        
        if not file_path.exists():
            raise ValueError(f"File does not exist: {filepath}")
        
        # Scan the parent directory but filter for this file
        parent_results = self.scan_directory(str(file_path.parent))
        return [r for r in parent_results if r.get("file") == str(file_path)]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of scan results."""
        return {
            "total_findings": len(self.results),
            "verified_credentials": sum(1 for r in self.results if r.get("verified", False)),
            "unique_detectors": len(set(r.get("detector", "Unknown") for r in self.results)),
            "severity_breakdown": {
                "HIGH": sum(1 for r in self.results if r.get("severity") == "HIGH"),
                "MEDIUM": sum(1 for r in self.results if r.get("severity") == "MEDIUM"),
                "LOW": sum(1 for r in self.results if r.get("severity") == "LOW"),
            }
        }
