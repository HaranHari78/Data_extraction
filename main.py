# main.py

from extractor import extract_data_from_csv

if __name__ == "__main__":
    input_file = "data/medicaldata.csv"
    extract_data_from_csv(input_file)
