import csv
import json
import os
import glob

# Input directory containing the CSV files
input_directory = "."  # Replace with your CSV directory path

# Output directory for JSON files
output_directory = "json_reviews"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to convert each CSV file to a JSON file
def csv_to_json(input_file, output_file):
    """Convert a single CSV file to a JSON file."""
    reviews = []
    try:
        # Read and parse the CSV file
        with open(input_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Skip the header row if present

            # Process each row and convert it to a structured dictionary
            for row in reader:
                try:
                    # Each row has the following format: [rating, title, body, date]
                    rating = row[0].strip()
                    title = row[1].strip()
                    body = row[2].strip()
                    date = row[3].strip()

                    # Create a structured JSON object for each review
                    review = {
                        "rating": rating,
                        "title": title,
                        "body": body,
                        "date": date
                    }

                    reviews.append(review)

                except IndexError:
                    print(f"Skipping malformed row in file {input_file}: {row}")

        # Save all reviews to a JSON file
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(reviews, jsonfile, ensure_ascii=False, indent=4)
        print(f"Successfully converted {input_file} to {output_file}")

    except Exception as e:
        print(f"Error processing {input_file}: {e}")

# Iterate through all sequentially named CSV files in the directory
for csv_file in sorted(glob.glob(os.path.join(input_directory, "trustpilot_reviews_page_*.csv"))):
    # Derive the JSON file name from the CSV file name
    base_name = os.path.basename(csv_file).replace(".csv", ".json")
    json_file = os.path.join(output_directory, base_name)

    # Convert the CSV file to a JSON file
    csv_to_json(csv_file, json_file)
