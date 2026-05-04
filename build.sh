#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Build the vector database from PDFs + synthetic medical data
python store_index.py
