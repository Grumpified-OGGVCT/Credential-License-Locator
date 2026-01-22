#!/usr/bin/env python3
"""
Command Line Interface for Credential-License-Locator

Provides a rich CLI experience for scanning credentials and licenses.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from credlicense.core.credential_scanner import CredentialScanner
from credlicense.core.license_scanner import LicenseScanner
from credlicense.ai.assistant import AIAssistant
from credlicense.utils.disclaimer import show_disclaimer
from credlicense.utils.report_generator import ReportGenerator


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    🔍 Credential-License-Locator
    
    A privacy-focused tool to scan for credentials and licenses in your local files.
    
    ⚠️  ETHICAL USE ONLY - Use responsibly and only on systems you own or have permission to scan.
    """
    pass


@main.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON)')
@click.option('--ai/--no-ai', default=False, help='Enable AI-powered analysis')
@click.option('--ai-provider', type=click.Choice(['ollama-cloud', 'ollama-local', 'openrouter']), 
              default='ollama-cloud', help='AI provider: Ollama CLOUD (default), local Ollama, or OpenRouter')
@click.option('--scan-type', type=click.Choice(['all', 'credentials', 'licenses']), 
              default='all', help='Type of scan to perform')
def scan(directory: str, output: Optional[str], ai: bool, ai_provider: str, scan_type: str):
    """
    Scan a directory for credentials and licenses.
    
    Example: credlicense scan /path/to/project --ai --output results.json
    """
    # Show ethical disclaimer
    if not show_disclaimer():
        console.print("[red]Scan cancelled by user.[/red]")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]Scanning: {directory}[/bold cyan]\n"
        f"Scan type: {scan_type}\n"
        f"AI Analysis: {'Enabled (' + ai_provider + ')' if ai else 'Disabled'}",
        title="Scan Configuration"
    ))
    
    results = {
        "directory": directory,
        "credentials": [],
        "licenses": [],
        "summary": {}
    }
    
    # Credential scanning
    if scan_type in ['all', 'credentials']:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning for credentials...", total=None)
            
            cred_scanner = CredentialScanner()
            try:
                results["credentials"] = cred_scanner.scan_directory(directory)
                progress.update(task, completed=True)
                console.print(f"[green]✓[/green] Found {len(results['credentials'])} potential credentials")
            except Exception as e:
                console.print(f"[red]✗[/red] Credential scan failed: {e}")
    
    # License scanning
    if scan_type in ['all', 'licenses']:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning for licenses...", total=None)
            
            lic_scanner = LicenseScanner()
            try:
                results["licenses"] = lic_scanner.scan_directory(directory)
                progress.update(task, completed=True)
                console.print(f"[green]✓[/green] Found {len(results['licenses'])} license references")
            except Exception as e:
                console.print(f"[red]✗[/red] License scan failed: {e}")
    
    # Display results
    _display_results(results)
    
    # AI Analysis
    if ai:
        console.print(f"\n[cyan]Running AI analysis with {ai_provider}...[/cyan]")
        ai_assistant = AIAssistant(provider=ai_provider)
        analysis = ai_assistant.analyze_findings(
            results["credentials"],
            results["licenses"]
        )
        
        if "error" in analysis:
            console.print(f"[yellow]AI Analysis failed: {analysis['error']}[/yellow]")
        else:
            console.print(Panel(
                analysis.get("analysis", "No analysis available"),
                title=f"AI Analysis ({analysis.get('provider', 'unknown')})",
                border_style="cyan"
            ))
            results["ai_analysis"] = analysis
    
    # Save results
    if output:
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"\n[green]Results saved to: {output}[/green]")
    
    # Generate summary
    _display_summary(results)


@main.command()
@click.argument('results_file', type=click.Path(exists=True))
@click.option('--format', type=click.Choice(['html', 'pdf', 'markdown']), 
              default='html', help='Report format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def report(results_file: str, format: str, output: Optional[str]):
    """
    Generate a report from scan results.
    
    Example: credlicense report results.json --format html --output report.html
    """
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        console.print(f"[red]Failed to load results: {e}[/red]")
        return
    
    generator = ReportGenerator()
    
    if not output:
        output = f"report.{format}"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Generating {format.upper()} report...", total=None)
        
        if format == 'html':
            generator.generate_html_report(results, output)
        elif format == 'markdown':
            generator.generate_markdown_report(results, output)
        else:
            console.print("[yellow]PDF format not yet implemented[/yellow]")
            return
        
        progress.update(task, completed=True)
    
    console.print(f"[green]Report generated: {output}[/green]")


@main.command()
def gui():
    """
    Launch the graphical user interface.
    """
    console.print("[cyan]Launching GUI...[/cyan]")
    from credlicense.ui.gui_app import launch_gui
    launch_gui()


@main.command()
def disclaimer():
    """
    Display the ethical use disclaimer.
    """
    show_disclaimer(force=True)


def _display_results(results: dict):
    """Display scan results in a formatted table."""
    
    # Credentials table
    if results["credentials"]:
        cred_table = Table(title="Credential Findings", show_header=True, header_style="bold magenta")
        cred_table.add_column("Detector", style="cyan")
        cred_table.add_column("File", style="green")
        cred_table.add_column("Severity", style="yellow")
        cred_table.add_column("Verified", style="red")
        
        for cred in results["credentials"][:20]:  # Show first 20
            cred_table.add_row(
                cred.get("detector", "Unknown"),
                str(Path(cred.get("file", "Unknown")).name),
                cred.get("severity", "UNKNOWN"),
                "✓" if cred.get("verified") else "✗"
            )
        
        console.print("\n")
        console.print(cred_table)
        
        if len(results["credentials"]) > 20:
            console.print(f"[dim]... and {len(results['credentials']) - 20} more[/dim]")
    
    # Licenses table
    if results["licenses"]:
        lic_table = Table(title="License Findings", show_header=True, header_style="bold blue")
        lic_table.add_column("Type", style="cyan")
        lic_table.add_column("License", style="green")
        lic_table.add_column("Source", style="yellow")
        
        for lic in results["licenses"][:20]:  # Show first 20
            source = lic.get("file", lic.get("package", "Unknown"))
            lic_table.add_row(
                lic.get("type", "Unknown"),
                lic.get("license", "Unknown"),
                str(Path(source).name) if lic.get("file") else source
            )
        
        console.print("\n")
        console.print(lic_table)
        
        if len(results["licenses"]) > 20:
            console.print(f"[dim]... and {len(results['licenses']) - 20} more[/dim]")


def _display_summary(results: dict):
    """Display a summary of scan results."""
    cred_count = len(results["credentials"])
    lic_count = len(results["licenses"])
    
    verified_creds = sum(1 for c in results["credentials"] if c.get("verified"))
    
    summary_text = f"""
[bold]Scan Summary[/bold]

Total Credentials Found: {cred_count}
  - Verified: {verified_creds}
  - Unverified: {cred_count - verified_creds}

Total License References: {lic_count}

[yellow]⚠️  Next Steps:[/yellow]
1. Review all verified credentials immediately
2. Rotate/revoke any exposed secrets
3. Implement proper secret management
4. Ensure license compliance for your project
"""
    
    console.print(Panel(summary_text, title="Summary", border_style="green"))


if __name__ == "__main__":
    main()
