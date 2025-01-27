import pandas as pd

def merge_datasets():
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

