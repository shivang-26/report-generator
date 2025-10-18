#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# No need to create output directory as we'll use /tmp
# Vercel's serverless environment provides a writable /tmp directory
