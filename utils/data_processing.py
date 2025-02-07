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

def process_personal_income_per_capital():
    # Load the CSV file
    file_path = "data/raw/Personal_Income_Per_Capital.csv"  # Replace with the path to your CSV file
    df = pd.read_csv(file_path)
    
    print(df.columns.tolist())

    # Filter columns for years 1999 to 2017, and include the 'State' column
    columns_to_keep = ['State'] + [str(year) for year in range(1999, 2018)]
    filtered_df = df[columns_to_keep]

    # Save the filtered data to a new CSV file
    filtered_df.to_csv("data/processed/Personal_Income_Per_Capital.csv", index=False)

    print(f"Filtered data saved to {filtered_df.head()}")

def process_median_income():
    # Read the Excel file into a DataFrame
    df = pd.read_excel("data/raw/Median_Household_Income.xls", header=[0, 1]) # read headers in row 1 and 2

    # Merge the two header levels: Keep only "Median income"
    df = df.loc[:, (df.columns.get_level_values(1) == "Median income") | (df.columns.get_level_values(0) == "State")]

    # Flatten and rename columns: Keep 'State' + years
    df.columns = ["State"] + [str(col[0]) for col in df.columns[1:]]  # Extract years from first header row

    # Filter only relevant years (1999–2017)
    columns_to_keep = ["State"] + [str(year) for year in range(1999, 2018)]
    df_filtered = df[columns_to_keep]

    # Reshape from wide to long format
    df_long = df_filtered.melt(id_vars=["State"], var_name="Year", value_name="Median Income")

    # Remove rows where "State" is NaN (if extra sheet duplicates exist)
    df_long = df_long.dropna(subset=["State"])

    # Save the processed data to a CSV file
    df_long.to_csv("data/processed/Median_Household_Income.csv", index=False)

    print(f"Processed data saved to {df_long.head()}")

def process_health_care_spending():
    # Read the Excel file into a DataFrame
    df = pd.read_excel("data/raw/Health_Care.xlsx", header=1) # header starts at row 2

    # Reshape DataFrame: Convert from wide to long format
    df_long = df.melt(id_vars=["Region/state of residence"], var_name="Year", value_name="Spending")
    df_long = df_long.rename(columns={"Region/state of residence": "State"})
    
    # Convert Year to string to match filtering range
    df_long["Year"] = df_long["Year"].astype(str)

    # Filter only for years 1999-2017
    df_filtered = df_long[df_long["Year"].isin([str(year) for year in range(1999, 2018)])]

    # Save the cleaned data to CSV
    df_filtered.to_csv("data/processed/Health_Care_Spending.csv", index=False)

    print(f"Processed data saved to {df_filtered.head()}")
