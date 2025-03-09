# db_utils.py
import pandas as pd
import sqlite3

def save_dataframe_to_sqlite(df, db_name, table_name='my_table', db_dir='db'):
    """
    Save a pandas DataFrame to an SQLite database with a timestamped filename.
    
    Parameters:
    - df (pd.DataFrame): The DataFrame to save.
    - db_name (str): Base name for the database file (without extension).
    - table_name (str): Name of the table to save the DataFrame into. Default is 'my_table'.
    - db_dir (str): Directory to store the database file. Default is 'db'.
    
    Returns:
    - str: Path to the created SQLite database file.
    """
    # Get today's date (without time)
    today_date = pd.Timestamp.today().date()

    # Create the database file path
    db_file_path = f"{db_dir}/Data_{db_name}_{today_date}.db"

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_file_path)

    try:
        # Save the DataFrame to the SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)
    finally:
        # Ensure the connection is closed
        conn.close()

    print(f"DataFrame has been saved to {db_file_path}")
    return db_file_path
