import pandas as pd

def merge_death_count_population():
    """
    Merges two datasets by Year and State and writes the result to a new CSV file.

    """
    try:
        # Load the datasets
        us_death_data = pd.read_csv("data/raw/US_Deaths.csv")
        us_population_data = pd.read_csv("data/raw/US_Populations.csv")
        
        # Exclude rows where Cause Name is "All Causes"
        us_death_data["Cause Name"] = us_death_data["Cause Name"].str.strip().str.lower()
        us_death_data = us_death_data[us_death_data["Cause Name"] != "all causes"]

        # Step 1: Handle missing or non-finite values
        us_death_data["Year"] = us_death_data["Year"].fillna(0)  # Replace NaN with 0
        us_death_data["Year"] = us_death_data["Year"].replace([float("inf"), float("-inf")], 0)  # Replace inf values with 0
        us_population_data["Year"] = us_population_data["Year"].fillna(0)

        # Step 2: Convert Year to integers
        # Ensure Year has the same data type
        us_death_data["Year"] = us_death_data["Year"].astype(int)
        us_population_data["Year"] = us_population_data["Year"].astype(int)

        # Merge the datasets
        merged_data = pd.merge(us_death_data, us_population_data, on=["Year", "State"], how="left")
        

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
        
def sum_all_death_states():
    # Load dataset
    df_death_cause = pd.read_csv("data/raw/US_Deaths.csv")
    df = pd.read_csv("data/processed/US_Deaths_Populations.csv", sep=",")
    df_filtered = df[df["State"] != "United States"]
    
    # Extract Age-Adjusted Death Rate for "All Causes"
    df_aadr = df_death_cause[df_death_cause["Cause Name"] == "All causes"][["Year", "State", "Age-adjusted Death Rate"]]

    # Sum deaths across all "Cause Name" for each (State, Year), and keep Population
    df_aggregated = (
        df_filtered.groupby(["Year", "State"], as_index=False)
        .agg({"Deaths": "sum", "Population": "first"})  # Summing Deaths, keeping Population
    )
    
    # Merge AADR into aggregated table
    df_aggregated = df_aggregated.merge(df_aadr, on=["Year", "State"], how="left")


    df_aggregated.to_csv("data/processed/States_Deaths_Populations.csv", index=False)
    
    print(df_aggregated.head())
    
def extract_poverty_rate():
    # Read the Excel file into a DataFrame
    df_poverty_full = pd.read_excel("data/raw/Poverty_Rate.xlsx", header=None)  # Read without a header to handle dynamic structures

    # Extract all row indices where years are present (assuming years are in column 0)
    year_rows = df_poverty_full[df_poverty_full[0].apply(lambda x: str(x).isdigit())].index

    # Initialize an empty list to store extracted data
    poverty_data = []

    # Loop through each year row and extract corresponding state data
    for i in range(len(year_rows)):
        year = int(df_poverty_full.iloc[year_rows[i], 0])  # Extract year
        start_idx = year_rows[i] + 1  # State data starts from the next row
        
        # Determine the end index (either the next year row or the end of the dataset)
        if i + 1 < len(year_rows):
            end_idx = year_rows[i + 1]
        else:
            end_idx = len(df_poverty_full)

        # Extract state-wise poverty data for the identified year
        state_data = df_poverty_full.iloc[start_idx:end_idx, [0, 4]]  # Column 0 = State, Column 4 = Poverty Rate
        state_data["Year"] = year  # Assign year
        
        # Rename columns properly
        state_data.columns = ["State", "Poverty Rate", "Year"]
        
        # Append to list
        poverty_data.append(state_data)

    # Concatenate all extracted data
    df_poverty_cleaned = pd.concat(poverty_data, ignore_index=True)

    # Remove any rows with missing values
    df_poverty_cleaned = df_poverty_cleaned.dropna()

    # Convert Poverty Rate to numeric
    df_poverty_cleaned["Poverty Rate"] = pd.to_numeric(df_poverty_cleaned["Poverty Rate"], errors="coerce")

    # Keep only data from 1999 to 2017
    df_poverty_cleaned = df_poverty_cleaned[(df_poverty_cleaned["Year"] >= 1999) & (df_poverty_cleaned["Year"] <= 2017)]
    df_poverty_cleaned = df_poverty_cleaned.dropna(subset=["Poverty Rate"])
    
    # Save the cleaned data to a CSV file
    df_poverty_cleaned.to_csv("data/processed/US_Poverty_Rate.csv", index=False)

    # Preview the cleaned data
    print(df_poverty_cleaned.head())

def process_personal_income_per_capita():
    df = pd.read_csv("data/raw/Personal_Income_Per_Capita.csv")
    
    print(df.columns.tolist())

    # Filter columns for years 1999 to 2017, and include the "State" column
    columns_to_keep = ['State'] + [str(year) for year in range(1999, 2018)]
    filtered_df = df[columns_to_keep]

    # Save the filtered data to a new CSV file
    filtered_df.to_csv("data/processed/Personal_Income_Per_Capita.csv", index=False)

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

def process_personal_health_care_per_capita():
    # Read the Excel file into a DataFrame
    df = pd.read_excel("data/raw/Personal_Health_Care_Per_Capita.xlsx", header=1) # header starts at row 2

    # Reshape DataFrame: Convert from wide to long format
    df_long = df.melt(id_vars=["Region/state of residence"], var_name="Year", value_name="Spending")
    df_long = df_long.rename(columns={"Region/state of residence": "State"})
    
    # Convert Year to string to match filtering range
    df_long["Year"] = df_long["Year"].astype(str)

    # Filter only for years 1999-2017
    df_filtered = df_long[df_long["Year"].isin([str(year) for year in range(1999, 2018)])]

    # Save the cleaned data to CSV
    df_filtered.to_csv("data/processed/Personal_Health_Care_Per_Capita.csv", index=False)

    print(f"Processed data saved to {df_filtered.head()}")

if __name__ == "__main__":
    sum_all_death_states()
