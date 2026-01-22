#!/bin/bash
# Example: Basic credential and license scan

echo "🔍 Credential-License-Locator - Basic Scan Example"
echo "=================================================="
echo ""

TARGET_DIR="${1:-./test_data}"
echo "Scanning directory: $TARGET_DIR"
echo ""

python -m credlicense.cli scan "$TARGET_DIR" --output scan-results.json
python -m credlicense.cli report scan-results.json --format html --output scan-report.html

echo ""
echo "✅ Done! Open scan-report.html in your browser"
