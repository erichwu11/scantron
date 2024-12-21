# ChatGPT generated
import csv

def count_elements_in_columns(file_path):
    """Count occurrences of each element in each column of a CSV file, starting from column three."""
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader, None)  # Get headers if present

            # Initialize a list of dictionaries for each column, starting from the third column
            column_counts = [{} for _ in headers[2:]] if headers else []

            for row in reader:
                for i, value in enumerate(row[2:], start=2):
                    if value in column_counts[i - 2]:
                        column_counts[i - 2][value] += 1
                    else:
                        column_counts[i - 2][value] = 1

            # Prepare results as a dictionary for columns starting from the third
            results = {
                headers[i]: column_counts[i - 2] if headers else column_counts[i - 2]
                for i in range(2, len(headers))
            }
            return results

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Example Usage
if __name__ == "__main__":
    file_path = "./output.csv"  # Replace with your CSV file path
    counts = count_elements_in_columns(file_path)
    for column, count in counts.items():
        print(f"Column '{column}': {count}")
