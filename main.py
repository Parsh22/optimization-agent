import zipfile
import os
import json
from collections import defaultdict

zip_file_path = '/Users/parshgoel/Desktop/nlp4lp.zip' 
extracted_dir = 'extracted_problems'  # Directory where the files will be extracted

# Step 1: Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir)

# Step 2: Walk through the extracted files and collect them
extracted_files = []
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        extracted_files.append(os.path.join(root, file))

# Step 3: Group the files by folder, keeping track of description.txt and input_targets.json
grouped_files = defaultdict(dict)

for file in extracted_files:
    folder = os.path.dirname(file)
    if file.endswith('description.txt'):
        grouped_files[folder]['description'] = file
    elif file.endswith('input_targets.json'):
        grouped_files[folder]['input_targets'] = file

# Step 4: Process the files and prepare them for fine-tuning in the chat format
fine_tune_data = []

for problem, files in grouped_files.items():
    # Only process if both description.txt and input_targets.json exist
    if 'description' in files and 'input_targets' in files:
        try:
            # Read description.txt
            with open(files['description'], 'r', encoding='utf-8') as desc_file:
                description_text = desc_file.read().strip()

            try:
                # Read input_targets.json
                with open(files['input_targets'], 'r', encoding='utf-8') as input_file:
                    input_targets_json = json.load(input_file)

                # Create a fine-tuning entry in the conversational format
                fine_tune_data.append({
                    "messages": [
                        {"role": "system", "content": "This is an LLM Agent for optimization problems."},
                        {"role": "user", "content": description_text},
                        {"role": "assistant", "content": json.dumps(input_targets_json)}  # JSON as a string
                    ]
                })

            except json.JSONDecodeError:
                print(f"Skipping {files['input_targets']} due to JSON decoding error.")

        except (UnicodeDecodeError, FileNotFoundError):
            print(f"Skipping {files['description']} due to encoding error or file not found.")

# Step 5: Save the processed data in JSONL format (fine-tuning format)
fine_tuning_file = 'fine_tune_chat_dataset.jsonl'  # Output file path

with open(fine_tuning_file, 'w', encoding='utf-8') as output_file:
    for entry in fine_tune_data:
        output_file.write(json.dumps(entry) + '\n')

print(f"Fine-tuning chat dataset has been saved to {fine_tuning_file}")
