#!/usr/bin/env python3
"""
AI Assistant Module

Integrates with Ollama (local) and OpenRouter (cloud) for AI-powered analysis.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional


class AIAssistant:
    """AI assistant for analyzing scan results and providing recommendations."""
    
    def __init__(self, provider: str = "ollama-cloud", openrouter_api_key: Optional[str] = None, 
                 ollama_api_key: Optional[str] = None):
        """
        Initialize AI assistant.
        
        Args:
            provider: AI provider to use - "ollama-cloud" (default), "ollama-local", or "openrouter"
            openrouter_api_key: API key for OpenRouter (from environment or parameter)
            ollama_api_key: API key for Ollama CLOUD (from environment or parameter)
        """
        self.provider = provider
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.ollama_api_key = ollama_api_key or os.getenv("OLLAMA_API_KEY")
        # Ollama CLOUD - full cloud API with advanced capabilities
        self.ollama_cloud_url = "https://api.ollama.cloud/v1/chat/completions"
        # Ollama LOCAL - simple local server connection
        self.ollama_local_url = os.getenv("OLLAMA_LOCAL_URL", "http://localhost:11434")
    
    def analyze_findings(self, credentials: List[Dict[str, Any]], 
                        licenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze scan findings using AI.
        
        Args:
            credentials: List of credential findings
            licenses: List of license findings
            
        Returns:
            Analysis results with recommendations
        """
        # Prepare summary for AI
        summary = self._prepare_summary(credentials, licenses)
        
        # Get AI analysis based on provider
        if self.provider == "ollama-cloud":
            analysis = self._analyze_with_ollama_cloud(summary)
        elif self.provider == "ollama-local":
            analysis = self._analyze_with_ollama_local(summary)
        elif self.provider == "openrouter":
            analysis = self._analyze_with_openrouter(summary)
        else:
            analysis = {"error": f"Unknown provider: {self.provider}. Use 'ollama-cloud', 'ollama-local', or 'openrouter'."}
        
        return analysis
    
    def _prepare_summary(self, credentials: List[Dict[str, Any]], 
                        licenses: List[Dict[str, Any]]) -> str:
        """Prepare a summary of findings for AI analysis."""
        credential_summary = f"Found {len(credentials)} potential credentials:\n"
        
        # Summarize by detector type
        detectors = {}
        for cred in credentials:
            detector = cred.get("detector", "Unknown")
            detectors[detector] = detectors.get(detector, 0) + 1
        
        for detector, count in detectors.items():
            credential_summary += f"  - {detector}: {count}\n"
        
        license_summary = f"\nFound {len(licenses)} license references:\n"
        
        # Summarize by license type
        license_types = {}
        for lic in licenses:
            license_name = lic.get("license", "Unknown")
            license_types[license_name] = license_types.get(license_name, 0) + 1
        
        for license_name, count in license_types.items():
            license_summary += f"  - {license_name}: {count}\n"
        
        return credential_summary + license_summary
    
    def _analyze_with_ollama_cloud(self, summary: str) -> Dict[str, Any]:
        """Analyze using Ollama CLOUD API - full cloud service with advanced capabilities."""
        if not self.ollama_api_key:
            return {"error": "Ollama CLOUD API key not provided. Set OLLAMA_API_KEY environment variable."}
        
        try:
            prompt = f"""You are a security expert analyzing scan results for credentials and licenses.

{summary}

Please provide:
1. Risk assessment (HIGH/MEDIUM/LOW)
2. Top 3 security recommendations
3. License compatibility concerns (if any)

Be concise and actionable."""

            headers = {
                "Authorization": f"Bearer {self.ollama_api_key}",
                "Content-Type": "application/json",
            }
            
            response = requests.post(
                self.ollama_cloud_url,
                headers=headers,
                json={
                    "model": "llama3.1:8b",  # Ollama Cloud model
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "provider": "ollama-cloud",
                    "analysis": result["choices"][0]["message"]["content"],
                    "model": "llama3.1:8b"
                }
            else:
                return {"error": f"Ollama CLOUD request failed: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Ollama CLOUD analysis failed: {str(e)}"}
    
    def _analyze_with_ollama_local(self, summary: str) -> Dict[str, Any]:
        """Analyze using local Ollama server - simple local connection for privacy-conscious users."""
        try:
            prompt = f"""You are a security expert analyzing scan results for credentials and licenses.

{summary}

Please provide:
1. Risk assessment (HIGH/MEDIUM/LOW)
2. Top 3 security recommendations
3. License compatibility concerns (if any)

Be concise and actionable."""

            # Simple local server connection - just sync and done
            response = requests.post(
                f"{self.ollama_local_url}/api/generate",
                json={
                    "model": "llama2",  # Default local model
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60  # Local can be slower
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "provider": "ollama-local",
                    "analysis": result.get("response", "No response from local Ollama"),
                    "model": "llama2",
                    "note": "Using local Ollama server (privacy mode)"
                }
            else:
                return {"error": f"Local Ollama request failed: {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            return {"error": f"Cannot connect to local Ollama at {self.ollama_local_url}. Make sure Ollama is running locally."}
        except Exception as e:
            return {"error": f"Local Ollama analysis failed: {str(e)}"}
    
    def _analyze_with_openrouter(self, summary: str) -> Dict[str, Any]:
        """Analyze using OpenRouter API."""
        try:
            prompt = f"""You are a security expert analyzing scan results for credentials and licenses.

{summary}

Please provide:
1. Risk assessment (HIGH/MEDIUM/LOW)
2. Top 3 security recommendations
3. License compatibility concerns (if any)

Be concise and actionable."""

            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/Grumpified-OGGVCT/Credential-License-Locator",
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct:free",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "provider": "openrouter",
                    "analysis": result["choices"][0]["message"]["content"],
                    "model": "meta-llama/llama-3.1-8b-instruct:free"
                }
            else:
                return {"error": f"OpenRouter request failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"OpenRouter analysis failed: {str(e)}"}
    
    def get_remediation_advice(self, finding: Dict[str, Any]) -> str:
        """Get specific remediation advice for a finding."""
        finding_type = finding.get("type")
        
        if finding_type == "credential":
            return self._get_credential_remediation(finding)
        elif finding_type in ["license_file", "license_header", "package_license"]:
            return self._get_license_remediation(finding)
        
        return "No specific remediation advice available."
    
    def _get_credential_remediation(self, finding: Dict[str, Any]) -> str:
        """Get remediation advice for credential findings."""
        detector = finding.get("detector", "Unknown")
        verified = finding.get("verified", False)
        
        advice = f"**Credential Detected: {detector}**\n\n"
        
        if verified:
            advice += "⚠️  **CRITICAL**: This credential is VERIFIED and actively usable!\n\n"
            advice += "Immediate actions:\n"
            advice += "1. Rotate/revoke this credential immediately\n"
            advice += "2. Review access logs for unauthorized usage\n"
            advice += "3. Remove from all files and version control history\n"
            advice += "4. Use environment variables or secret management systems\n"
        else:
            advice += "Actions:\n"
            advice += "1. Verify if this is a real credential\n"
            advice += "2. If real, rotate/revoke immediately\n"
            advice += "3. Remove from files and use proper secret management\n"
            advice += "4. Add to .gitignore or equivalent\n"
        
        return advice
    
    def _get_license_remediation(self, finding: Dict[str, Any]) -> str:
        """Get remediation advice for license findings."""
        license_name = finding.get("license", "Unknown")
        
        advice = f"**License: {license_name}**\n\n"
        
        # Basic license guidance
        license_guidance = {
            "MIT": "Permissive license. Can be used freely with attribution.",
            "Apache-2.0": "Permissive license. Requires attribution and license notice.",
            "GPL-3.0": "Copyleft license. Derivative works must be GPL-3.0.",
            "GPL-2.0": "Copyleft license. Derivative works must be GPL-2.0.",
            "BSD-3-Clause": "Permissive license. Similar to MIT with additional clause.",
            "AGPL-3.0": "Strong copyleft. Network use triggers distribution requirements.",
        }
        
        if license_name in license_guidance:
            advice += license_guidance[license_name] + "\n\n"
        
        advice += "Actions:\n"
        advice += "1. Ensure license compliance in your project\n"
        advice += "2. Include required attribution/notices\n"
        advice += "3. Check compatibility with your project's license\n"
        advice += "4. Document all dependencies and their licenses\n"
        
        return advice
