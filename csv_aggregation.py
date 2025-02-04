import csv
import argparse
import pprint


def convert_type(value):
    """Converts a string value to int, float, or keeps it as a string."""
    if value.strip() == "":  # Handle empty strings
        return None

    # Check for integers (including negative numbers)
    if value.lstrip('-').isdigit():
        return int(value)

    # Check for floats (including negative float numbers)
    if value.lstrip('-').replace('.', '', 1).isdigit():
        return float(value)

    return value  # Return as string if no conversion is possible


def read_csv_data(file_path):
    """Reads a CSV file and returns headers and data rows."""
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = [row for row in reader]
    return headers, data


def aggregate_data(headers, data):
    """Computes sum, average, min, max, and count for numeric columns.
       If a column contains strings, its aggregation returns default values.
    """
    numeric_columns = {col: [] for col in headers}
    column_types = {col: None for col in headers}  # Track column type

    for row in data:
        for i, value in enumerate(row):
            converted_value = convert_type(value)

            if isinstance(converted_value, (int, float)):
                numeric_columns[headers[i]].append(converted_value)
                column_types[headers[i]] = "numeric"  # Mark column as numeric
            else:
                column_types[headers[i]] = "string"  # Mark column as string

    # Compute aggregation
    results = {}
    for col, values in numeric_columns.items():
        if column_types[col] == "numeric" and values:  # Numeric column with values
            results[col] = {
                "Sum": sum(values),
                "Average": sum(values) / len(values),
                "Min": min(values),
                "Max": max(values),
                "Count": len(values),
            }
        else:  # String or empty column
            results[col] = {
                "Sum": None,
                "Average": None,
                "Min": None,
                "Max": None,
                "Count": 0,
            }

    return results


def main():
    parser = argparse.ArgumentParser(description="Aggregate numeric data from a CSV file.")
    parser.add_argument("--file", type=str, required=True, help="Path to the CSV file.")
    
    args = parser.parse_args()
    file_path = args.file
    
    try:
        headers, data = read_csv_data(file_path)
        aggregated_results = aggregate_data(headers, data)

        # Print results in a readable format
        pprint.pprint(aggregated_results)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()