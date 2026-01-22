#!/usr/bin/env python3
"""
Graphical User Interface for Credential-License-Locator

Provides an innovative and user-friendly GUI experience.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
from pathlib import Path
from datetime import datetime

from credlicense.core.credential_scanner import CredentialScanner
from credlicense.core.license_scanner import LicenseScanner
from credlicense.ai.assistant import AIAssistant
from credlicense.utils.disclaimer import DISCLAIMER_TEXT
from credlicense.utils.report_generator import ReportGenerator


class CredentialLicenseGUI:
    """Main GUI application for Credential-License-Locator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Credential-License-Locator")
        self.root.geometry("1200x800")
        
        # Results storage
        self.results = {
            "credentials": [],
            "licenses": [],
            "directory": ""
        }
        
        self.scanning = False
        
        # Setup UI
        self._setup_ui()
        
        # Show disclaimer on startup
        self._show_disclaimer()
    
    def _setup_ui(self):
        """Setup the user interface."""
        # Create main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header
        self._create_header(main_container)
        
        # Control Panel
        self._create_control_panel(main_container)
        
        # Results Area (Notebook with tabs)
        self._create_results_area(main_container)
        
        # Status Bar
        self._create_status_bar(main_container)
    
    def _create_header(self, parent):
        """Create header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="🔍 Credential-License-Locator",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Scan for credentials and licenses in your local directories",
            font=("Helvetica", 12)
        )
        subtitle_label.pack()
    
    def _create_control_panel(self, parent):
        """Create control panel with scan options."""
        control_frame = ttk.LabelFrame(parent, text="Scan Configuration", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Directory selection
        dir_frame = ttk.Frame(control_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="Directory:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=60)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(dir_frame, text="Browse...", command=self._browse_directory).pack(side=tk.LEFT)
        
        # Options frame
        options_frame = ttk.Frame(control_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Scan type
        ttk.Label(options_frame, text="Scan Type:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.scan_type_var = tk.StringVar(value="all")
        scan_types = [("All", "all"), ("Credentials Only", "credentials"), ("Licenses Only", "licenses")]
        
        for text, value in scan_types:
            ttk.Radiobutton(
                options_frame,
                text=text,
                variable=self.scan_type_var,
                value=value
            ).pack(side=tk.LEFT, padx=5)
        
        # AI options
        ai_frame = ttk.Frame(control_frame)
        ai_frame.pack(fill=tk.X, pady=5)
        
        self.ai_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            ai_frame,
            text="Enable AI Analysis",
            variable=self.ai_enabled_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(ai_frame, text="AI Provider:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.ai_provider_var = tk.StringVar(value="ollama-cloud")
        ttk.Radiobutton(ai_frame, text="Ollama CLOUD", variable=self.ai_provider_var, value="ollama-cloud").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ai_frame, text="Ollama Local", variable=self.ai_provider_var, value="ollama-local").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(ai_frame, text="OpenRouter", variable=self.ai_provider_var, value="openrouter").pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.scan_button = ttk.Button(
            button_frame,
            text="🔍 Start Scan",
            command=self._start_scan,
            style="Accent.TButton"
        )
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop",
            command=self._stop_scan,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📄 Export Report",
            command=self._export_report
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="⚠️ Show Disclaimer",
            command=self._show_disclaimer
        ).pack(side=tk.LEFT)
    
    def _create_results_area(self, parent):
        """Create results display area with tabs."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Summary Tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text="📊 Summary")
        self._create_summary_tab()
        
        # Credentials Tab
        self.credentials_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.credentials_tab, text="🔐 Credentials")
        self._create_credentials_tab()
        
        # Licenses Tab
        self.licenses_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.licenses_tab, text="📜 Licenses")
        self._create_licenses_tab()
        
        # AI Analysis Tab
        self.ai_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ai_tab, text="🤖 AI Analysis")
        self._create_ai_tab()
    
    def _create_summary_tab(self):
        """Create summary tab content."""
        self.summary_text = scrolledtext.ScrolledText(
            self.summary_tab,
            wrap=tk.WORD,
            font=("Courier", 10),
            state=tk.DISABLED
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial message
        self._update_summary_text("No scan results yet. Configure and start a scan to see results.")
    
    def _create_credentials_tab(self):
        """Create credentials tab with tree view."""
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(self.credentials_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ("Detector", "File", "Line", "Severity", "Verified")
        self.cred_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Define headings
        self.cred_tree.heading("Detector", text="Detector")
        self.cred_tree.heading("File", text="File")
        self.cred_tree.heading("Line", text="Line")
        self.cred_tree.heading("Severity", text="Severity")
        self.cred_tree.heading("Verified", text="Verified")
        
        # Column widths
        self.cred_tree.column("Detector", width=150)
        self.cred_tree.column("File", width=300)
        self.cred_tree.column("Line", width=80)
        self.cred_tree.column("Severity", width=100)
        self.cred_tree.column("Verified", width=80)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.cred_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.cred_tree.xview)
        self.cred_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.cred_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
    
    def _create_licenses_tab(self):
        """Create licenses tab with tree view."""
        tree_frame = ttk.Frame(self.licenses_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Type", "License", "Source", "Confidence")
        self.lic_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        self.lic_tree.heading("Type", text="Type")
        self.lic_tree.heading("License", text="License")
        self.lic_tree.heading("Source", text="Source")
        self.lic_tree.heading("Confidence", text="Confidence")
        
        self.lic_tree.column("Type", width=150)
        self.lic_tree.column("License", width=150)
        self.lic_tree.column("Source", width=300)
        self.lic_tree.column("Confidence", width=100)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.lic_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.lic_tree.xview)
        self.lic_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.lic_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
    
    def _create_ai_tab(self):
        """Create AI analysis tab."""
        self.ai_text = scrolledtext.ScrolledText(
            self.ai_tab,
            wrap=tk.WORD,
            font=("Courier", 10),
            state=tk.DISABLED
        )
        self.ai_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._update_ai_text("AI analysis will appear here after scan completion (if enabled).")
    
    def _create_status_bar(self, parent):
        """Create status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate', length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.dir_var.set(directory)
    
    def _show_disclaimer(self):
        """Show ethical use disclaimer."""
        disclaimer_window = tk.Toplevel(self.root)
        disclaimer_window.title("Ethical Use Disclaimer")
        disclaimer_window.geometry("700x600")
        
        text_widget = scrolledtext.ScrolledText(
            disclaimer_window,
            wrap=tk.WORD,
            font=("Courier", 10),
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", DISCLAIMER_TEXT)
        text_widget.configure(state=tk.DISABLED)
        
        button_frame = ttk.Frame(disclaimer_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            button_frame,
            text="I Understand and Agree",
            command=disclaimer_window.destroy
        ).pack()
    
    def _start_scan(self):
        """Start the scanning process."""
        directory = self.dir_var.get()
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory to scan.")
            return
        
        if not Path(directory).exists():
            messagebox.showerror("Error", "Selected directory does not exist.")
            return
        
        # Disable scan button, enable stop button
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning = True
        
        # Start progress bar
        self.progress_bar.start()
        
        # Run scan in separate thread
        scan_thread = threading.Thread(target=self._perform_scan, args=(directory,))
        scan_thread.start()
    
    def _perform_scan(self, directory):
        """Perform the actual scanning (runs in separate thread)."""
        try:
            self._update_status("Scanning for credentials...")
            
            scan_type = self.scan_type_var.get()
            
            # Credential scanning
            if scan_type in ['all', 'credentials'] and self.scanning:
                cred_scanner = CredentialScanner()
                self.results["credentials"] = cred_scanner.scan_directory(directory)
            
            if not self.scanning:
                return
            
            self._update_status("Scanning for licenses...")
            
            # License scanning
            if scan_type in ['all', 'licenses'] and self.scanning:
                lic_scanner = LicenseScanner()
                self.results["licenses"] = lic_scanner.scan_directory(directory)
            
            if not self.scanning:
                return
            
            self.results["directory"] = directory
            
            # AI Analysis
            if self.ai_enabled_var.get() and self.scanning:
                self._update_status("Running AI analysis...")
                
                provider = self.ai_provider_var.get()
                ai_assistant = AIAssistant(provider=provider)
                
                ai_result = ai_assistant.analyze_findings(
                    self.results["credentials"],
                    self.results["licenses"]
                )
                
                self.results["ai_analysis"] = ai_result
            
            # Update UI with results
            if self.scanning:
                self.root.after(0, self._display_results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Scan Error", f"An error occurred: {str(e)}"))
        finally:
            self.root.after(0, self._scan_complete)
    
    def _stop_scan(self):
        """Stop the scanning process."""
        self.scanning = False
        self._scan_complete()
        messagebox.showinfo("Scan Stopped", "Scan process has been stopped.")
    
    def _scan_complete(self):
        """Called when scan is complete."""
        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()
        self._update_status("Scan complete")
    
    def _display_results(self):
        """Display scan results in the UI."""
        # Update summary
        summary = self._generate_summary()
        self._update_summary_text(summary)
        
        # Update credentials tree
        self._populate_credentials_tree()
        
        # Update licenses tree
        self._populate_licenses_tree()
        
        # Update AI analysis
        if "ai_analysis" in self.results:
            ai_analysis = self.results["ai_analysis"]
            if "error" in ai_analysis:
                self._update_ai_text(f"AI Analysis Error: {ai_analysis['error']}")
            else:
                self._update_ai_text(
                    f"Provider: {ai_analysis.get('provider', 'Unknown')}\n"
                    f"Model: {ai_analysis.get('model', 'Unknown')}\n\n"
                    f"{ai_analysis.get('analysis', 'No analysis available')}"
                )
    
    def _generate_summary(self):
        """Generate summary text."""
        creds = self.results.get("credentials", [])
        lics = self.results.get("licenses", [])
        
        verified = sum(1 for c in creds if c.get("verified", False))
        
        summary = f"""
SCAN SUMMARY
{'=' * 60}

Directory: {self.results.get('directory', 'Unknown')}
Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CREDENTIALS:
  Total Found: {len(creds)}
  Verified: {verified}
  Unverified: {len(creds) - verified}

LICENSES:
  Total Found: {len(lics)}
  
"""
        
        if verified > 0:
            summary += f"\n⚠️  WARNING: {verified} VERIFIED credential(s) found!\n"
            summary += "These are actively usable and should be rotated IMMEDIATELY!\n"
        
        return summary
    
    def _populate_credentials_tree(self):
        """Populate credentials tree view."""
        # Clear existing items
        for item in self.cred_tree.get_children():
            self.cred_tree.delete(item)
        
        # Add new items
        for cred in self.results.get("credentials", []):
            verified_mark = "✓" if cred.get("verified", False) else "✗"
            
            self.cred_tree.insert("", "end", values=(
                cred.get("detector", "Unknown"),
                Path(cred.get("file", "Unknown")).name,
                cred.get("line", "N/A"),
                cred.get("severity", "UNKNOWN"),
                verified_mark
            ))
    
    def _populate_licenses_tree(self):
        """Populate licenses tree view."""
        # Clear existing items
        for item in self.lic_tree.get_children():
            self.lic_tree.delete(item)
        
        # Add new items
        for lic in self.results.get("licenses", []):
            source = lic.get("file", lic.get("package", "Unknown"))
            source_display = Path(source).name if lic.get("file") else source
            
            self.lic_tree.insert("", "end", values=(
                lic.get("type", "Unknown"),
                lic.get("license", "Unknown"),
                source_display,
                lic.get("confidence", "N/A")
            ))
    
    def _update_summary_text(self, text):
        """Update summary text widget."""
        self.summary_text.configure(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", text)
        self.summary_text.configure(state=tk.DISABLED)
    
    def _update_ai_text(self, text):
        """Update AI analysis text widget."""
        self.ai_text.configure(state=tk.NORMAL)
        self.ai_text.delete("1.0", tk.END)
        self.ai_text.insert("1.0", text)
        self.ai_text.configure(state=tk.DISABLED)
    
    def _update_status(self, message):
        """Update status bar message."""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def _export_report(self):
        """Export results to a file."""
        if not self.results.get("credentials") and not self.results.get("licenses"):
            messagebox.showwarning("No Results", "No scan results to export. Please run a scan first.")
            return
        
        # Ask for file format
        format_window = tk.Toplevel(self.root)
        format_window.title("Export Report")
        format_window.geometry("300x150")
        
        ttk.Label(format_window, text="Select export format:", font=("Helvetica", 12)).pack(pady=10)
        
        format_var = tk.StringVar(value="html")
        
        ttk.Radiobutton(format_window, text="HTML Report", variable=format_var, value="html").pack(pady=5)
        ttk.Radiobutton(format_window, text="Markdown Report", variable=format_var, value="markdown").pack(pady=5)
        ttk.Radiobutton(format_window, text="JSON Data", variable=format_var, value="json").pack(pady=5)
        
        def do_export():
            format_window.destroy()
            
            # File dialog
            if format_var.get() == "html":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".html",
                    filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
                )
            elif format_var.get() == "markdown":
                filename = filedialog.asksaveasfilename(
                    defaultextension=".md",
                    filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
                )
            else:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
            
            if filename:
                try:
                    if format_var.get() == "json":
                        with open(filename, 'w') as f:
                            json.dump(self.results, f, indent=2)
                    else:
                        generator = ReportGenerator()
                        if format_var.get() == "html":
                            generator.generate_html_report(self.results, filename)
                        else:
                            generator.generate_markdown_report(self.results, filename)
                    
                    messagebox.showinfo("Export Complete", f"Report exported to:\n{filename}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export report:\n{str(e)}")
        
        ttk.Button(format_window, text="Export", command=do_export).pack(pady=10)


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    CredentialLicenseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
