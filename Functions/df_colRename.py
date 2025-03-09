import pandas as pd

def colrename_Transpose(df, rename_dict):
    """
    Processes a DataFrame by renaming columns, transposing, and formatting the index.

    Parameters:
        df (pd.DataFrame): The input DataFrame to process, must be unindexed with column to convert 'economy' to 'year'
        rename_dict (dict): A dictionary where keys are the current column names 
                            and values are the new column names.

    Returns:
        pd.DataFrame: A transformed DataFrame with renamed columns, transposed, and indexed by datetime.
    """
    # Rename columns using the provided dictionary
    df.rename(columns=rename_dict, inplace=True)
    
    # Set the index, transposing without indexing will create a phantom row and push the original columns to the first row
    #df.set_index("year", inplace=True)
    
    # Transpose the DataFrame
    df = df.T
    
    # Reset the index to create a column named 'year'
    df.reset_index(inplace=True)

    # Rename the index column to 'year'
    df.rename(columns={"index": "year"}, inplace=True)
    
    #try:
    #    if "index" in df.columns and "year" not in df.columns:
    #        df.rename(columns={"index": "year"}, inplace=True)
    #    if "year" in df.columns:
    #        df.set_index("year", inplace=True)
    #except Exception as e:
    #    print(f"Error: {e}")

    # Convert the 'year' column to datetime
    df["year"] = pd.to_datetime(df["year"])

    # Set the 'year' column as the index
    df.set_index("year", inplace=True)

    return df

'''
# Example usage
# Create a sample DataFrame
data = {
    "economy": ["US", "China", "Japan", "Germany", "India"],
    "YR2014": [17000, 10300, 4600, 4000, 2000],
    "YR2015": [18000, 10800, 4800, 4200, 2100],
    "YR2016": [18500, 11200, 5000, 4400, 2200],
    "YR2017": [19000, 11500, 5200, 4600, 2300],
}
df_input = pd.DataFrame(data)

# Define the rename dictionary
rename_dict = {
    "economy": "year",
    "YR2014": "2014",
    "YR2015": "2015",
    "YR2016": "2016",
    "YR2017": "2017",
}

# Call the function
df_processed = process_dataframe(df_input, rename_dict)

# Output the result
print(df_processed.info())
print(df_processed)
'''