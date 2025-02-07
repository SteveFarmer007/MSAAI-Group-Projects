import pandas as pd

def merge_death_count_population():
    """
    Merges two datasets by Year and State and writes the result to a new CSV file.

    """
    try:
        # Load the datasets
        us_death_data = pd.read_csv('data/raw/US_Deaths.csv')
        us_population_data = pd.read_csv('data/raw/US_Populations.csv')

        # Step 1: Handle missing or non-finite values
        us_death_data['Year'] = us_death_data['Year'].fillna(0)  # Replace NaN with 0
        us_death_data['Year'] = us_death_data['Year'].replace([float('inf'), float('-inf')], 0)  # Replace inf values with 0
        us_population_data['Year'] = us_population_data['Year'].fillna(0)

        # Step 2: Convert Year to integers
        # Ensure Year has the same data type
        us_death_data['Year'] = us_death_data['Year'].astype(int)
        us_population_data['Year'] = us_population_data['Year'].astype(int)

        # Merge the datasets
        merged_data = pd.merge(us_death_data, us_population_data, on=['Year', 'State'], how='left')

        # Check for missing values after the merge
        missing_values = merged_data.isnull().sum()
        if missing_values.any():
            print("Warning: Missing values detected after merging. Check your data.")
            print(missing_values)

        # Save the merged dataset to a new CSV file
        merged_data.to_csv('data/processed/US_Deaths_Populations.csv', index=False)
        print(f"Merged dataset successfully saved to: US_Deaths_Populations.csv")

    except Exception as e:
        print(f"An error occurred: {e}")
        
def extract_poverty_rate():
    # Path to your Excel file
    excel_file = "data/raw/Poverty_Rate.xlsx"  # Replace with your file path

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file, engine="openpyxl")  # Read without a header to handle dynamic structures

    # Initialize an empty list to store cleaned data
    cleaned_data = []

    # Iterate through the rows to detect years and associate rows below them
    current_year = None
    for index, row in df.iterrows():
        # Check if the row contains the year
        first_cell = row[0]
        if isinstance(first_cell, int) and 1999 <= first_cell <= 2017:
            current_year = first_cell  # Extract the year (integer)
        elif isinstance(first_cell, str) and first_cell.isdigit() and 1999 <= int(first_cell) <= 2017:
            current_year = int(first_cell)  # Extract the year (string converted to integer)
        elif current_year:
            # Extract relevant data rows after detecting a year
            state = row[0]  # state is in the first column
            poverty_rate = row[4]  # poverty rate is in the fifth column
            
            # **Skip rows that look like column headers**
            if isinstance(state, str) and "state" in state.lower():
                continue  # Skip header-like rows
        
            if pd.notnull(state) and pd.notnull(poverty_rate):  # Ensure data is not empty
                cleaned_data.append({"Year": current_year, "State": state, "Poverty Rate": poverty_rate})

    # Convert cleaned data into a DataFrame
    cleaned_df = pd.DataFrame(cleaned_data)

    # Save the cleaned data to a CSV file
    cleaned_df.to_csv("data/processed/US_Poverty_Rate.csv", index=False)

    # Preview the cleaned data
    print(cleaned_df.head())


# Call the function if the script is run directly
if __name__ == "__main__":
    extract_poverty_rate()  