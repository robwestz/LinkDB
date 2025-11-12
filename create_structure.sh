#!/bin/bash

# Skapa mappar
mkdir -p data/input
mkdir -p data/output

# Skapa tomma filer
touch build_customer_db.py
touch export_ai_packets.py
touch settings.py
touch data/input/Main_lanksheet.xlsx
touch data/output/linkops.db
touch data/output/summary.md

echo "Projektstruktur skapad!"
echo "linkdb/"
echo "├── build_customer_db.py"
echo "├── export_ai_packets.py"
echo "├── settings.py"
echo "└── data/"
echo "    ├── input/"
echo "    │   └── Main_lanksheet.xlsx"
echo "    └── output/"
echo "        ├── linkops.db"
echo "        └── summary.md"