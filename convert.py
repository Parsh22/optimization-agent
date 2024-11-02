# import csv
# import json

# def convert_csv_to_training_format(input_csv, output_file):
#     system_message = {
#         "role": "system",
#         "content": "This is an LLM Agent for optimization problems"
#     }

#     with open(input_csv, 'r', encoding='utf-8') as csvfile, \
#          open(output_file, 'w', encoding='utf-8') as outfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip header

#         for row in reader:
#             medical_report = row[0]
#             extracted_json = row[1]

#             training_example = {
#                 "messages": [
#                     system_message,
#                     {"role": "user", "content": medical_report},
#                     {"role": "assistant", "content": extracted_json}
#                 ]
#             }
#             outfile.write(json.dumps(training_example) + '\n')
            
# convert_csv_to_training_format("./data.csv", "./train.jsonl")

import csv
import json

def convert_csv_to_training_format(input_csv, output_file):
    system_message = {
        "role": "system",
        "content": "This is an LLM Agent for optimization problems"
    }

    def clean_text(text):
        # Removes leading/trailing whitespace, excessive internal whitespace, and newline characters
        return ' '.join(text.split())

    with open(input_csv, 'r', encoding='utf-8') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header

        for row in reader:
            # Clean the data to remove unwanted whitespace and new lines
            medical_report = clean_text(row[0])
            extracted_json = clean_text(row[1])

            training_example = {
                "messages": [
                    system_message,
                    {"role": "user", "content": medical_report},
                    {"role": "assistant", "content": extracted_json}
                ]
            }
            outfile.write(json.dumps(training_example) + '\n')

convert_csv_to_training_format("./dataNl4Opt.csv", "./train.jsonl")
