# Disaster Response Pipeline

## by José Manuel García 

## Project of the Udacity Data Science Nanodegree
------------------------------------------

### Project Overview
This project aims to analyze disaster data to build a model for an API that classifies disaster messages making use of pipelines for preprocessing data and creating the Machine Learning models.

### Files in the repository
- process_data.py: ETL Pipeline that loads messages and categories datasets, merges them, cleans the data, and stores it in a SQL database.
- train_classifier.py: Machine Learning Pipeline that loads data from the previous database, splits it into training and testing, and creates the model with cited data using GridSearchCV for the model tunning.
- run.py: final script which takes all the previous work and creates a web to interact with it.

### Instructions to use the code stored in 'workspace' folder:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
