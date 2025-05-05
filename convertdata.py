import pandas as pd

def xlsx_to_csv(xlsx_filepath, csv_filepath):
  """
  Converts an XLSX file to a CSV file.

  Args:
    xlsx_filepath (str): The path to the input XLSX file.
    csv_filepath (str): The path to the output CSV file.
  """
  try:
    df = pd.read_excel(xlsx_filepath)
    df.to_csv(csv_filepath, index=False, encoding='utf-8')
    print(f"Successfully converted '{xlsx_filepath}' to '{csv_filepath}'")
  except FileNotFoundError:
    print(f"Error: File not found at '{xlsx_filepath}'")
  except Exception as e:
    print(f"An error occurred: {e}")

if __name__ == "__main__":
  input_xlsx_file = "dataall.xlsx"
  output_csv_file = "dataall.csv"
  xlsx_to_csv(input_xlsx_file, output_csv_file)
  print(f"\nConversion complete. The CSV file '{output_csv_file}' has been created in the same folder.")
