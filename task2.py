import pandas as pd
import glob

def main():
    # Read all CSV files from data directory
    dfs = [pd.read_csv(f) for f in ["./data/daily_sales_data_0.csv", "./data/daily_sales_data_1.csv", "./data/daily_sales_data_2.csv"]]
    df = pd.concat(dfs, ignore_index=True)

    # Filter for pink morsel
    df = df[df['product'].str.contains('pink morsel', case=False, na=False)]

    # Create sales column and select required columns
    df['price'] = df['price'].str.replace('$', '').astype(float)
    df['sales'] = '$' + (df['quantity'] * df['price']).astype(str)
    output = df[['sales', 'date', 'region']]

    # Write to output file
    output.to_csv('./data/output.csv', index=False)

if __name__ == "__main__":
    main()