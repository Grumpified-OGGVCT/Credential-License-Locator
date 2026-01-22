#!/usr/bin/env python3
"""
Sample file with an API key for testing credential detection.
"""

import os

# WARNING: This is a fake API key for testing purposes only
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def connect_to_api():
    """Connect to API using credentials."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-API-Key": API_KEY
    }
    return headers

def get_aws_client():
    """Get AWS client with credentials."""
    return {
        "access_key": AWS_ACCESS_KEY,
        "secret_key": SECRET_KEY
    }
