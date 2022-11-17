from etl.etl import ETL

num_batches = 20 # Number of batches to process
ETL().run_etl_task(num_batches)

print("Done")
