# # import json
# # import csv

# # def create_jsonl_data(description, background_constraints_parameters, data):
# #     system_content = "This is an LLM Agent for optimization problems"

# #     # Parse the JSON data
# #     bcp_data = json.loads(background_constraints_parameters)
# #     data_json = json.loads(data)

# #     # Replace parameter placeholders with actual values in the description
# #     user_content = description
# #     for param in bcp_data['parameters']:
# #         symbol = param['symbol']
# #         if symbol in data_json:
# #             user_content = user_content.replace(f"\\param{{{symbol}}}", str(data_json[symbol]))

# #     # Update parameter values
# #     for param in bcp_data['parameters']:
# #         symbol = param['symbol']
# #         if symbol in data_json:
# #             param['value'] = data_json[symbol]

# #     # Create the assistant content
# #     assistant_content = json.dumps({
# #         "background": bcp_data['background'],
# #         "constraints": bcp_data['constraints'],
# #         "objective": bcp_data['objective'],
# #         "parameters": bcp_data['parameters']
# #     })

# #     # Create the final JSONL structure
# #     jsonl_data = {
# #         "messages": [
# #             {"role": "system", "content": system_content},
# #             {"role": "user", "content": user_content},
# #             {"role": "assistant", "content": assistant_content}
# #         ]
# #     }

# #     return json.dumps(jsonl_data)

# # # Read the CSV file and process each row
# # with open('nlp4lp.csv', 'r') as csvfile:
# #     csvreader = csv.reader(csvfile)
# #     next(csvreader)  # Skip header row if present
    
# #     with open('nlp4lpProcessed.jsonl', 'w') as jsonl_file:
# #         for row in csvreader:
# #             description = row[0]
# #             background_constraints_parameters = row[1]
# #             data = row[2]
            
# #             jsonl_output = create_jsonl_data(description, background_constraints_parameters, data)
# #             jsonl_file.write(jsonl_output + '\n')

# # print("JSONL data has been generated and saved to output.jsonl")

# import json
# import csv

# def create_jsonl_data(description, background_constraints_parameters, data):
#     system_content = "This is an LLM Agent for optimization problems"

#     # Parse the JSON data
#     bcp_data = json.loads(background_constraints_parameters)
#     data_json = json.loads(data)

#     # Replace parameter placeholders with actual values in the description
#     user_content = description
#     for param, value in data_json.items():
#         user_content = user_content.replace(f"\\param{{{param}}}", str(value))

#     # Remove any remaining backslashes
#     user_content = user_content.replace("\\", "")

#     # Update parameter values in bcp_data
#     for param in bcp_data['parameters']:
#         symbol = param['symbol']
#         if symbol in data_json:
#             param['value'] = data_json[symbol]

#     # Create the assistant content
#     assistant_content = json.dumps({
#         "background": bcp_data['background'],
#         "constraints": bcp_data['constraints'],
#         "objective": bcp_data['objective'],
#         "parameters": bcp_data['parameters']
#     })

#     # Create the final JSONL structure
#     jsonl_data = {
#         "messages": [
#             {"role": "system", "content": system_content},
#             {"role": "user", "content": user_content},
#             {"role": "assistant", "content": assistant_content}
#         ]
#     }

#     return json.dumps(jsonl_data)

# # Read the CSV file and process each row
# with open('nlp4lp.csv', 'r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     next(csvreader)  # Skip header row if present
    
#     with open('nlp4lpProcessed.jsonl', 'w') as jsonl_file:
#         for row in csvreader:
#             description = row[0]
#             background_constraints_parameters = row[1]
#             data = row[2]
            
#             jsonl_output = create_jsonl_data(description, background_constraints_parameters, data)
#             jsonl_file.write(jsonl_output + '\n')

# print("JSONL data has been generated and saved to output.jsonl")

import json
import csv
import re

def create_jsonl_data(description, background_constraints_parameters, data):
    system_content = "This is an LLM Agent for optimization problems"

    # Parse the JSON data
    bcp_data = json.loads(background_constraints_parameters)
    data_json = json.loads(data)

    # Replace parameter placeholders with actual values in the description
    for param, value in data_json.items():
        placeholder = f"\\param{{{param}}}"
        description = description.replace(placeholder, str(value))

    # Remove any remaining backslashes
    description = description.replace("\\", "")

    # Update parameter values in bcp_data
    for param in bcp_data['parameters']:
        symbol = param['symbol']
        if symbol in data_json:
            param['value'] = data_json[symbol]

    # Create the assistant content
    assistant_content = json.dumps({
        "background": bcp_data['background'],
        "constraints": bcp_data['constraints'],
        "objective": bcp_data['objective'],
        "parameters": bcp_data['parameters']
    })

    # Create the final JSONL structure
    jsonl_data = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": description},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    return json.dumps(jsonl_data)

def read_csv_file(file_path):
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row if present
        for row in csvreader:
            yield row

def process_csv(input_file, output_file):
    with open(output_file, 'w') as jsonl_file:
        for row in read_csv_file(input_file):
            if len(row) != 3:
                print(f"Skipping invalid row: {row}")
                continue

            description, background_constraints_parameters, data = row

            try:
                jsonl_output = create_jsonl_data(description, background_constraints_parameters, data)
                jsonl_file.write(jsonl_output + '\n')
            except json.JSONDecodeError as e:
                print(f"Error processing row: {e}")
                print(f"Problematic data: {background_constraints_parameters}")

if __name__ == "__main__":
    input_csv = "nlp4lp.csv"
    output_jsonl = "nlp4lpProcessed.jsonl"
    process_csv(input_csv, output_jsonl)
    print(f"JSONL data has been generated and saved to {output_jsonl}")