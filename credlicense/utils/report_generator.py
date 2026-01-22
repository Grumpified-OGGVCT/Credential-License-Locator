#!/usr/bin/env python3
"""
Report Generator Module

Generates reports in various formats from scan results.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ReportGenerator:
    """Generate reports from scan results in various formats."""
    
    def generate_html_report(self, results: Dict[str, Any], output_path: str):
        """Generate an HTML report."""
        html_content = self._build_html_report(results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def generate_markdown_report(self, results: Dict[str, Any], output_path: str):
        """Generate a Markdown report."""
        md_content = self._build_markdown_report(results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def _build_html_report(self, results: Dict[str, Any]) -> str:
        """Build HTML report content."""
        credentials = results.get("credentials", [])
        licenses = results.get("licenses", [])
        ai_analysis = results.get("ai_analysis", {})
        
        # Count statistics
        total_creds = len(credentials)
        verified_creds = sum(1 for c in credentials if c.get("verified", False))
        total_licenses = len(licenses)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Credential & License Scan Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th {{
            background-color: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .severity-high {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .severity-medium {{
            color: #f39c12;
            font-weight: bold;
        }}
        .severity-low {{
            color: #3498db;
        }}
        .verified {{
            color: #e74c3c;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding: 20px;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Credential & License Scan Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>Directory: {results.get('directory', 'Unknown')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_creds}</div>
            <div class="stat-label">Potential Credentials</div>
        </div>
        <div class="stat-card">
            <div class="stat-number severity-high">{verified_creds}</div>
            <div class="stat-label">Verified Credentials</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_licenses}</div>
            <div class="stat-label">License References</div>
        </div>
    </div>
"""

        # Warning for verified credentials
        if verified_creds > 0:
            html += f"""
    <div class="warning">
        <strong>⚠️ CRITICAL:</strong> {verified_creds} verified credential(s) found! 
        These are actively usable and should be rotated immediately.
    </div>
"""

        # AI Analysis
        if ai_analysis and "analysis" in ai_analysis:
            html += f"""
    <div class="section">
        <h2>🤖 AI Analysis</h2>
        <p><strong>Provider:</strong> {ai_analysis.get('provider', 'Unknown')}</p>
        <p><strong>Model:</strong> {ai_analysis.get('model', 'Unknown')}</p>
        <pre style="white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 4px;">{ai_analysis.get('analysis', '')}</pre>
    </div>
"""

        # Credentials table
        if credentials:
            html += """
    <div class="section">
        <h2>🔐 Credential Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Detector</th>
                    <th>File</th>
                    <th>Line</th>
                    <th>Severity</th>
                    <th>Verified</th>
                </tr>
            </thead>
            <tbody>
"""
            for cred in credentials:
                severity_class = f"severity-{cred.get('severity', 'low').lower()}"
                verified_mark = "✓" if cred.get("verified", False) else "✗"
                verified_class = "verified" if cred.get("verified", False) else ""
                
                html += f"""
                <tr>
                    <td>{cred.get('detector', 'Unknown')}</td>
                    <td>{Path(cred.get('file', 'Unknown')).name}</td>
                    <td>{cred.get('line', 'N/A')}</td>
                    <td class="{severity_class}">{cred.get('severity', 'UNKNOWN')}</td>
                    <td class="{verified_class}">{verified_mark}</td>
                </tr>
"""
            html += """
            </tbody>
        </table>
    </div>
"""

        # Licenses table
        if licenses:
            html += """
    <div class="section">
        <h2>📜 License Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th>License</th>
                    <th>Source</th>
                    <th>Confidence</th>
                </tr>
            </thead>
            <tbody>
"""
            for lic in licenses:
                source = lic.get("file", lic.get("package", "Unknown"))
                source_display = Path(source).name if lic.get("file") else source
                
                html += f"""
                <tr>
                    <td>{lic.get('type', 'Unknown')}</td>
                    <td>{lic.get('license', 'Unknown')}</td>
                    <td>{source_display}</td>
                    <td>{lic.get('confidence', 'N/A')}</td>
                </tr>
"""
            html += """
            </tbody>
        </table>
    </div>
"""

        html += """
    <div class="footer">
        <p>Generated by Credential-License-Locator</p>
        <p><em>Use responsibly and ethically. Only scan systems you own.</em></p>
    </div>
</body>
</html>
"""
        return html
    
    def _build_markdown_report(self, results: Dict[str, Any]) -> str:
        """Build Markdown report content."""
        credentials = results.get("credentials", [])
        licenses = results.get("licenses", [])
        ai_analysis = results.get("ai_analysis", {})
        
        md = f"""# Credential & License Scan Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Directory:** {results.get('directory', 'Unknown')}

---

## Summary

- **Total Credentials Found:** {len(credentials)}
- **Verified Credentials:** {sum(1 for c in credentials if c.get('verified', False))}
- **Total License References:** {len(licenses)}

"""

        # AI Analysis
        if ai_analysis and "analysis" in ai_analysis:
            md += f"""## AI Analysis

**Provider:** {ai_analysis.get('provider', 'Unknown')}  
**Model:** {ai_analysis.get('model', 'Unknown')}

{ai_analysis.get('analysis', '')}

---

"""

        # Credentials
        if credentials:
            md += """## Credential Findings

| Detector | File | Line | Severity | Verified |
|----------|------|------|----------|----------|
"""
            for cred in credentials:
                verified_mark = "✓" if cred.get("verified", False) else "✗"
                md += f"| {cred.get('detector', 'Unknown')} | {Path(cred.get('file', 'Unknown')).name} | {cred.get('line', 'N/A')} | {cred.get('severity', 'UNKNOWN')} | {verified_mark} |\n"
            
            md += "\n---\n\n"

        # Licenses
        if licenses:
            md += """## License Findings

| Type | License | Source | Confidence |
|------|---------|--------|------------|
"""
            for lic in licenses:
                source = lic.get("file", lic.get("package", "Unknown"))
                source_display = Path(source).name if lic.get("file") else source
                md += f"| {lic.get('type', 'Unknown')} | {lic.get('license', 'Unknown')} | {source_display} | {lic.get('confidence', 'N/A')} |\n"
            
            md += "\n---\n\n"

        md += """
---

*Generated by Credential-License-Locator*  
*Use responsibly and ethically. Only scan systems you own.*
"""
        
        return md
