import pandas as pd
import glob
import os

def read_files(directory):
    file_paths = glob.glob(f"{directory}/*.csv")
    dataframes = []
    
    for path in file_paths:
        data_all = pd.read_csv(path)
        len(data_all)
        
        # Filter for only Pink Morsels
        filt = data_all["product"] == "pink morsel"
        data_pink_morsel = data_all.loc[filt].copy()

        # remove $ from price and convert to float
        data_pink_morsel['price'] = data_pink_morsel['price'].str.replace('$', '').astype(float)

        # Calculate sales
        data_pink_morsel['sales'] = (data_pink_morsel['quantity'] * data_pink_morsel['price']).astype(float)
    
        # Select only the necessary columns
        data_with_necessary_cols = data_pink_morsel[['sales', 'date','region']]
        
        # # Append the DataFrame to the list
        dataframes.append(data_with_necessary_cols)   

        # # Concatenate all DataFrames into a single DataFrame
        final_df = pd.concat(dataframes, ignore_index=True)

        # sort data by date
        final_df = final_df.sort_values('date')

        # Create the output directory if it doesn't exist
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
    
        # Save the final DataFrame to a new CSV file inside the output directory
        final_df.to_csv(os.path.join(output_dir, "sales_data.csv"), index=False)




read_files("data")


