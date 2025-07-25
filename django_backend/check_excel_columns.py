import pandas as pd
import os

def check_excel_columns(file_path, file_name):
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            print(f"\n{file_name}:")
            print(f"Columns: {df.columns.tolist()}")
            print(f"First few rows:")
            print(df.head(2))
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
    else:
        print(f"{file_name} not found")

data_dir = "data"
files_to_check = [
    ("FCADIPA.xlsx", "Properties"),
    ("FIMIPA2.xlsx", "FIMIPA IPRA"),
    ("tblp.xlsx", "Construction Prices"),
    ("FENDEREC.xlsx", "Addresses")
]

for filename, description in files_to_check:
    check_excel_columns(os.path.join(data_dir, filename), f"{description} ({filename})")
