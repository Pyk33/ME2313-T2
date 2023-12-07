import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Directory containing the downloaded CSV files
raw_data_directory = os.path.expanduser("~/Desktop/Trioptima/Raw data")

# Output directory for categorized CSV files
output_directory = os.path.expanduser("~/Desktop/Trioptima/Categorized Data")

# List of keywords to categorize CSV files
categories = ['RT.COMMODITY']  #'RT.CDS', 'RT.EQUITY', 'RT.IRS', RT.FX,

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Function to process a single file and return a category dataframe
def process_file(file_path, category):
    try:
        df = pd.read_csv(file_path, dtype=str)
        df.replace('nan', '', inplace=True)
        return category, df
    except pd.errors.ParserError as e:
        print(f"Error processing {file_path}: {e}")
        return category, pd.DataFrame()

# Iterate through categories
for category in categories:
    # Dictionary to store data frames for the current category
    category_dataframes = {category: pd.DataFrame()}
    
    category_directory = os.path.join(raw_data_directory, category)
    if os.path.exists(category_directory):
        processed_files_count = 0  # Reset processed files count for the current category
        
        with ThreadPoolExecutor() as executor:
            # Process files in parallel using ThreadPoolExecutor
            futures = []
            for filename in os.listdir(category_directory):
                if filename.lower().endswith('.csv'):
                    file_path = os.path.join(category_directory, filename)
                    futures.append(executor.submit(process_file, file_path, category))

            # Retrieve results from futures and update category dataframes
            for future in futures:
                category, df = future.result()
                category_dataframes[category] = pd.concat([category_dataframes[category], df], sort=False)

                # Increment the processed files count
                processed_files_count += 1

                # Print the count of processed files after each file
                print(f"Processed {processed_files_count} files from {category} category.")

        # Save data frames to a separate CSV file for the current category
        category_output_path = os.path.join(output_directory, f"{category}_Data.csv")
        category_dataframes[category].to_csv(category_output_path, index=False)
        print(f"{category} Data saved at: {category_output_path}")
    else:
        print(f"Category directory not found: {category_directory}")
