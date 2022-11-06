# Technical Assessment
## `Lead Data Manager`
## Overview

At Memorable, we work predicting the cognitive impact of images and videos to optimize advertising strategies. Everyday, our data infrastructure receives new data points in the form of model scores, metadata and files, which have to be properly processed before making them available to our teams. This test will evaluate your ability to develop an ETL process matching some of Memorable's current challenges. 

### The Task

In this task we will simulate 20 iterations of an ETL job that seeks to compute a client-facing metric based on our models' output to include it in our dashboard. For the task, you are expected to build a pipeline that receives the sequence of batches as an input, reading them in order, and at each iteration computes a `percentile` according to the task description.

**Extraction**
Under the `batches/` directory you will find 20 batches of scored assets (400 assets per batch) that simulate 20 extraction jobs from our deployed inference pipeline.

Each item in the batch will include the following data:

- `id` : a ULID identifying the scored asset
- `score` : represents the output of a machine learning model for one of our metrics
- `industry` : represents the industry to which that asset belongs, can be one of 
    - Clothing
    - Food
    - Cars
    - Hair care


Data is being extracted without any preprocessing step, so you can assume you are working with the raw version of the data. This includes potentially misspelled categories and micomputed scores.

**Transformation**
The model score is not an interpretable metric for our clients, as the number is not capped and there are hints of potential drifts in the model's output, given that new trends in advertising cause assets to score higher as time passes by. For this reason, we want to implement a process that converts the scores to percentiles, which are capped between 0 and 100 and help the client clearly compare 2 different scores and judge them good or bad.

From previous ad hoc analyses, our team has identified that the four industries follow Normal distributions with different parameters, so percentile computation should take this into account and **percentiles should be computed based on the asset's corresponding industry distribution**.

Moreover, we have also identified certain design trends in the uploaded assets that bias the model scores and cause an incremental drift in its output, biasing later scored assets to be higher than previous ones. To account for this shift and allow comparisons between old and new assets, **percentiles should be updated for all the received scores at any time and computed using as an input only the data belonging to the latest 3 batches of scored assets**.

**Loading**
The output of the transformation should be loaded in a singel SQL table with the following schema:
- `id` : column to store the asset IDs, which uniquely identify each asset processed.
- `score` : column to store the model's output for that asset
- `industry` : column to store the asset's industry
- `percentile` : the updated version of the scores percentile following the indications in the previous section.

To increase traceability on the evolution of the scores' drift, a second table should be maintained to keep track of how the percentile evolves for each asset (identified with the `id`). The schema for this second table looks like:
- `id`: column to store the asset IDs, which uniquely identify each asset processed.
- `score`: column to store the model's output for that asset
- `industry`: column to store the asset's industry
- `percentile`: the updated version of the scores percentile following the indications in the previous section.
- `update_iteration`: the iteration number at which this value is updated.


#### Example
The value at `updated_iteration` helps to tag the iteration at which the `percentile` score was updated. For example, when *batch_4* is loaded, the percentiles will be computed using the industry scores from *batches batch_2, batch_3 and batch_4* and the iteration value will be 4 (iteration 0 happens at initialization with *batch_0*).


### Delivery
Once you have cloned this repository, close it and create a new one from your own Github user. This will ensure that your deliverable will not be visible to other candidates. Failing to close the repository and/or overwriting any content in the `master` branch of this repository will result in immediate disqualification.

Once the task is completed, please ensure to add the following users as collaborators:
- [JHevia23](https://github.com/JHevia23)
- [ppfreitas](https://github.com/ppfreitas)
- [cfosco](https://github.com/cfosco)
    
and notify by email to your recruiting contact. As part of the deliverable, you are expected to share the resulting table in a format of your choosing. It can be a SQL file, a parquet file, a CSV or any you find most suitable.

## Evaluation criteria
We take a holistic approach to evaluation and these are the main components:

- `Effectiveness` : whether the delivered development effectively tackles the proposed task and the output matches expected results.
- `Efficiency` : whether the delivered development addresses recommended practices for software development. Use of standard technologies is also recommended. 
- `Documentation`: Clear documentation and commented code account for a significant part of the evaluation. It will also allow us to understand your thought process better and consider it as part of our evaluation criteria.