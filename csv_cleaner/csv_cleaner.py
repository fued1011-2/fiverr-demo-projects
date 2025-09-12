import pandas as pd

def clean_csv(input_file, output_file):
    # Load CSV or Excel
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Unsupported file type. Use .csv or .xlsx")
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Drop completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Save as same format
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    else:
        raise ValueError("Unsupported output file type. Use .csv or .xlsx")

if __name__ == "__main__":
    # Example usage
    clean_csv("input.csv", "output_clean.csv")
