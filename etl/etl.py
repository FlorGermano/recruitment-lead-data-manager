import os
import numpy as np
import pandas as pd
from typing import Tuple

class ETL:

    def __init__(self):
        self.industries = ['clothing', 'food', 'cars', 'hair care']
        self.input_files = 'batches/batch' # Path to the json files
        self.scores_table_file = 'scores_table.csv' # Main output table
        self.scores_table_columns = ['id', 'score', 'industry', 'percentile'] # Columns for the main output table

    def run_etl_task(self, num_batches: int):
        """
        Extracts, transforms the data calculating percentiles and then loads it into the scores_table.csv file
        Parameters:
        num_batches: Number of batches to process
        """
        data = pd.DataFrame()
        # Iterate through batches
        for run_id in range(num_batches):
            # Extract data
            data = self.__extract_data(data, run_id)
            # Transform data
            transformed_data = self.__transform_data(data, run_id)
            # Load data
            self.__load_data(transformed_data, run_id)
            

    def __extract_data(self, data: pd.DataFrame, run_id: int) -> pd.DataFrame:
        """
        Extract data from new batch and append it to data from the last two batches
        """
        # Keep previous data only of the 2 last batches
        if run_id > 2:
            data = data.loc[data['run_id'] >= run_id - 2]
        # Read data
        new_data = pd.read_json(f"{self.input_files}_{str(run_id)}.json")
        # Convert score to numeric
        new_data['score'] = pd.to_numeric(new_data['score'], errors='coerce')
        # Add run_id field
        new_data['run_id'] = run_id
        # Append to previous data
        return pd.concat([data, new_data])
    

    def __transform_data(self, data: pd.DataFrame, run_id: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Transform data computing percentiles per industry when possible
        """
        if (run_id >= 2) : # Calculate percentiles only after at least 3 batches were processed
            # Iterate through industries
            for industry in self.industries:
                # Create percentiles per industry
                data.loc[data['industry'] == industry, 'percentile'] = pd.qcut(data.loc[data['industry'] == industry]['score'], 100, labels=range(0, 100))
        else:
            data['percentile'] = '-1'
        # Return transformed data from the current batch
        return data.loc[data['run_id'] == run_id]

    def __load_data(self, data: pd.DataFrame, run_id: int) -> None:
        """
        Load data into scores_table and historical_percentiles_table
        """
        # Append data from last batch into scores table
        data.loc[data['run_id'] == run_id][self.scores_table_columns].to_csv(
            self.scores_table_file, mode='a', index=False, quotechar='|', header=not os.path.exists(f"./{self.scores_table_file}")
        )
        # Append percentiles per asset and run_id to historical percentages table to keep track of the scores' drift
        data[['run_id', 'id', 'percentile']].to_csv(
            'historical_percentiles_table.csv', mode='a', index=False, quotechar='|', header=not os.path.exists(f"./historical_percentiles_table.csv")
        )
        