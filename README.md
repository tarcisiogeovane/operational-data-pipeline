# Project: Operational Data Pipeline Simulation (Oil & Gas)

This project simulates a complete, end-to-end data pipeline for an oilfield drilling operation. It's designed to mimic the flow of data from rig sensors to a final, interactive dashboard that a drilling engineer or manager would use to monitor performance.


## Simulated Scenario

We are monitoring two drilling rigs (___RIG-001___ and ___RIG-002___) as they drill a new well (___WELL-101A___). Our sensors on the rig are capturing data every few minutes:

- Depth: Current depth of the drill bit.

- ROP (Rate of Penetration): How fast the drill is advancing.

- WOB (Weight on Bit): Force applied to the drill bit.

- Torque: Rotational force of the drill string.

- Mud Pressure: Pressure of the drilling fluid.

This raw data is exported as a ___raw_sensor_data.csv___ file. Our job is to build a pipeline that automatically cleans this data, calculates key performance metrics, stores it in a database, and displays it on a live dashboard.


## Project Architecture

#### 1. Data Collection (___/scripts/data_collection.py___)
- A Python script that simulates raw sensor data.

- It generates a CSV file named raw_sensor_data.csv to act as our "source" data.

#### 2. ETL Pipeline (___/etl_pipeline.ipynb___)
- A Jupyter Notebook that performs the Extract, Transform, and Load (ETL) process.

- Extract: Reads the ___raw_sensor_data.csv___.

- Transform: Cleans the data, converts data types, and engineers a new feature: drilling_efficiency.

- Load: Saves the cleaned, transformed data into a SQLite database (oilfield_data.db).

#### 3. Database (___oilfield_data.db___)
- A simple, file-based SQLite database that stores our clean "production-ready" data.


#### 4. Dashboard (___/dashboard.py___)

- A web-based, interactive dashboard built with Streamlit.

- It reads directly from the oilfield_data.db to visualize KPIs, charts, and trends.

## How to Run This Project

### 1. Setup Your Environment:

- Make sure you have Python 3.7+ installed.

- Create a virtual environment (recommended):

``` 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- Install the required libraries:
```
pip install -r requirements.txt
```

### 1. Step 1: Generate Raw Data
Run the data collection script. This will create raw_sensor_data.csv in your project's root folder.
```
python scripts/data_collection.py
```

### 2. Step 2: Run the ETL Pipeline

- Run the Jupyter Notebook to process the raw data and create the database.
- Start Jupyter:
```
jupyter notebook
```

- Open etl_pipeline.ipynb in your browser and run all the cells. This will create the oilfield_data.db file.

### 3. Step 3: Launch the Dashboard

- Run the Streamlit app from your terminal:
```
streamlit run dashboard.py
```

- Your web browser will automatically open to the live, interactive dashboard!
