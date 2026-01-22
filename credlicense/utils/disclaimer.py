#!/usr/bin/env python3
"""
Ethical Use Disclaimer Module

Displays important warnings and disclaimers about ethical use.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm


console = Console()


DISCLAIMER_TEXT = """
[bold red]⚠️  ETHICAL USE DISCLAIMER ⚠️[/bold red]

This tool is designed to help you:
✓ Find and secure YOUR OWN credentials
✓ Organize YOUR OWN software licenses
✓ Audit systems YOU OWN or have EXPLICIT PERMISSION to scan

[bold yellow]PROHIBITED USES:[/bold yellow]
✗ Scanning systems you don't own
✗ Unauthorized access to others' credentials
✗ Any illegal or unethical activities
✗ Violating terms of service or agreements

[bold cyan]LEGAL RESPONSIBILITY:[/bold cyan]
• You are solely responsible for how you use this tool
• Unauthorized access to computer systems is illegal
• Respect privacy and intellectual property rights
• Only scan systems you own or have written permission to scan

[bold green]BEST PRACTICES:[/bold green]
• Use environment variables for API keys
• Never commit secrets to version control
• Rotate credentials immediately if exposed
• Implement proper secret management systems
• Keep all findings confidential and secure

By using this tool, you acknowledge that you have read and agree to use it
responsibly and in compliance with all applicable laws and regulations.
"""


def show_disclaimer(force: bool = False) -> bool:
    """
    Display the ethical use disclaimer and get user consent.
    
    Args:
        force: If True, show disclaimer without requiring confirmation
        
    Returns:
        True if user accepts, False otherwise
    """
    console.print(Panel(
        DISCLAIMER_TEXT,
        title="[bold]Credential-License-Locator - Ethical Use Agreement[/bold]",
        border_style="red",
        padding=(1, 2)
    ))
    
    if force:
        return True
    
    try:
        return Confirm.ask("\n[bold]Do you acknowledge and agree to use this tool ethically and legally?[/bold]")
    except KeyboardInterrupt:
        console.print("\n[bold red]Disclaimer prompt interrupted. Exiting.[/bold red]")
        return False


def show_security_warning():
    """Display security best practices warning."""
    warning = """
[bold yellow]🔒 SECURITY BEST PRACTICES[/bold yellow]

If credentials are found:
1. [red]IMMEDIATE ACTION REQUIRED[/red] - Rotate/revoke ALL exposed credentials
2. Review access logs for potential unauthorized access
3. Remove credentials from files and version control history
4. Implement proper secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
5. Use environment variables or secret management systems
6. Never commit secrets to version control
7. Enable secret scanning in your CI/CD pipeline

Remember: Prevention is better than detection!
"""
    
    console.print(Panel(warning, border_style="yellow"))
