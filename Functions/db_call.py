import os
import sqlite3
import pandas as pd  # Ensure pandas is imported for DataFrame operations

def manage_sqlite_db(relative_project_dir='.', db_name = 'default' , table_name='my_table'):
    """
    Function to manage SQLite database connection, fetch data, and return a DataFrame.

    Parameters:
        relative_project_dir (str): Relative directory containing the database folder.
        db_name (str): Name of the SQLite database (without extension).
        table_name (str): Name of the table to fetch data from.

    Returns:
        pd.DataFrame: DataFrame containing data from the specified table.
    """
    # Save the current working directory
    original_dir = os.getcwd()

    try:
        # Compute absolute path for the project directory
        project_dir = os.path.abspath(relative_project_dir)

        # Ensure the database folder exists
        db_folder = os.path.join(project_dir, 'db')
        os.makedirs(db_folder, exist_ok=True)

        # Full path to the database file
        db_file_path = os.path.join(db_folder, db_name + '.db')
        print(f"Database file path: {db_file_path}")

        # Connect to SQLite database or create it
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Query data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Close the database connection
        conn.close()

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Reset to the original directory
        os.chdir(original_dir)

# Example usage
# relative_dir = './my_project'
# database_name = 'Data_US-GDP'
# table_name = 'your_table_name_here'  # Replace with the actual table name
# df = manage_sqlite_db(relative_dir, database_name, table_name)
# print(df)


'''
def manage_sqlite_db(project_dir, db_name,table_name='my_table',):
    """
    Function to manage SQLite database connection, fetch data, and return a DataFrame.

    Parameters:
        project_dir (str): Directory containing the database folder.
        db_name (str): Name of the SQLite database (without extension).
        table_name (str): Name of the table to fetch data from.

    Returns:
        pd.DataFrame: DataFrame containing data from the specified table.
    """
    # Save the current working directory
    original_dir = os.getcwd()

    try:
        # Change to the project directory
        os.chdir(project_dir)

        # Ensure the database folder exists
        db_folder = os.path.join(project_dir, 'db')
        os.makedirs(db_folder, exist_ok=True)

        # Full path to the database file
        db_file_path = os.path.join(db_folder, db_name + '.db')
        print(f"Database file path: {db_file_path}")

        # Connect to SQLite database or create it
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Query data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Close the database connection
        conn.close()

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Reset to the original directory
        os.chdir(original_dir)

# Example usage

# project_directory = '/Users/matthiaschia/Library/CloudStorage/GoogleDrive-matthias0991@gmail.com/My Drive/02_Projects/09_Portfolio_Thesis'
# database_name = 'Data_US-GDP'
# table_name = 'your_table_name_here'  # Replace with the actual table name
# df = manage_sqlite_db(project_directory, database_name, table_name)
# print(df)
'''