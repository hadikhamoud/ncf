import os
import json
import pandas as pd
from pathlib import Path
import argparse

def read_json_files_guardian(directory):
    data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = Path(root) / file
                with open(file_path) as f:
                    content = json.load(f)
                    results = content.get("response", {}).get("results", [])
                    for result in results:
                        fields = result.get("fields", {})
                        result.update(fields)
                        del result["fields"]
                        data.append(result)
    return data

def main():
    parser = argparse.ArgumentParser(description='Convert JSON files to a CSV file.')
    parser.add_argument('--directory', help='Directory containing JSON files')
    parser.add_argument('--output_csv', help='Output CSV file path')

    args = parser.parse_args()

    data = read_json_files_guardian(args.directory)
    df = pd.DataFrame(data)
    df.to_csv(args.output_csv, index=False)
    print(f"Data has been written to {args.output_csv}")

if __name__ == "__main__":
    main()