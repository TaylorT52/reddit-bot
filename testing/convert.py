import json
import csv

# Input and output files
input_file = "logs/flagged.json"    # Your NDJSON file
output_file = "output.csv"   # Resulting CSV

# Read and parse each line as a JSON object
with open(input_file, "r") as f:
    records = [json.loads(line) for line in f]

# Write CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
