import json
import csv
import pandas as pd # pandas is often easier for this kind of transformation

# --- Method 1: Using pandas (Recommended for simplicity and flexibility) ---
def json_to_csv_pandas(json_file_path, csv_file_path):
    """
    Converts a JSON file (as described in the problem) to a CSV file using pandas.
    Each conversation turn becomes a row in the CSV.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}. Check file format.")
        return

    all_conversation_turns = []
    turn_id_counter = 0 # To create a unique ID for each turn

    for topic_data in raw_data:
        topic_name = topic_data.get('topic', 'Unknown Topic') # Get topic name
        conversations = topic_data.get('conversations', [])

        for conv_turn in conversations:
            turn_id_counter += 1
            turn_data = {
                'turn_id': turn_id_counter,
                'topic': topic_name,
                'speaker': conv_turn.get('speaker'),
                'gujlish': conv_turn.get('gujlish'),
                'english': conv_turn.get('english')
            }
            all_conversation_turns.append(turn_data)

    if not all_conversation_turns:
        print("No conversation data found in the JSON file.")
        return

    # Create a pandas DataFrame
    df = pd.DataFrame(all_conversation_turns)

    # Save to CSV
    try:
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        print(f"Successfully converted '{json_file_path}' to '{csv_file_path}' using pandas.")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# --- Method 2: Using the `csv` module (More manual) ---
def json_to_csv_manual(json_file_path, csv_file_path):
    """
    Converts a JSON file (as described in the problem) to a CSV file
    using the built-in csv module.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}. Check file format.")
        return

    # Define CSV headers
    headers = ['turn_id', 'topic', 'speaker', 'gujlish', 'english']
    turn_id_counter = 0

    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader() # Write the header row

            for topic_data in raw_data:
                topic_name = topic_data.get('topic', 'Unknown Topic')
                conversations = topic_data.get('conversations', [])

                for conv_turn in conversations:
                    turn_id_counter += 1
                    row_data = {
                        'turn_id': turn_id_counter,
                        'topic': topic_name,
                        'speaker': conv_turn.get('speaker'),
                        'gujlish': conv_turn.get('gujlish'),
                        'english': conv_turn.get('english')
                    }
                    writer.writerow(row_data)
        print(f"Successfully converted '{json_file_path}' to '{csv_file_path}' using csv module.")
    except IOError:
        print(f"Error: Could not write to CSV file at {csv_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # Replace 'corpus.json' with the actual path to your JSON file
    input_json_file = 'gujlishConversationalDataset.json'

    # Define output CSV file paths
    output_csv_pandas = 'corpus_pandas.csv'
    output_csv_manual = 'corpus_manual.csv'

    print("--- Using pandas method ---")
    json_to_csv_pandas(input_json_file, output_csv_pandas)

    # print("\n--- Using manual csv module method ---")
    # json_to_csv_manual(input_json_file, output_csv_manual)

    # You can then inspect the generated CSV files.
    # For example, to quickly see the first few lines of the pandas-generated CSV:
    try:
        df_check = pd.read_csv(output_csv_pandas)
        print(f"\n--- First 5 rows of '{output_csv_pandas}' ---")
        print(df_check.head())
    except FileNotFoundError:
        print(f"\nCould not read '{output_csv_pandas}' to display head.")