import os
import json

def get_ids_from_json(json_data):
    ids = []

    for item in json_data['response']['results']:
            if 'id' in item:
                ids.append(item['id'])
    return ids


def get_ids_from_json_nyt(json_data):
    ids = []

    for item in json_data['response']['docs']:
            if '_id' in item:
                ids.append(item['_id'])
    return ids




def find_json_files(directory_path):
    json_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def extract_ids(json_files):
    unique_ids = set()
    for json_file in json_files:
        with open(json_file, 'r') as file:
            try:
                json_data = json.load(file)
                ids = get_ids_from_json_nyt(json_data)
                unique_ids.update(ids)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_file}: {e}")
    return unique_ids

def main():
    directory_path = 'data/nyt'
    json_files = find_json_files(directory_path)
    unique_ids = extract_ids(json_files)
    print(f"Total unique IDs: {len(unique_ids)}")

if __name__ == "__main__":
    main()
