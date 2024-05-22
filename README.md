# UN Dashboard
This repository contains the code for a UN Dashboard that visualizes datasets related to GDP, Unemployment, Population, and Education for various countries.

## Features
- **Choropleth Map**: View data on a world map.
- **Bar Chart**: Display bar charts for selected countries and datasets.
- **Line Chart**: Compare data across multiple countries over time.

## Deployed Dashboard

Access the deployed UN Dashboard at [https://un-dashboard.onrender.com/](https://un-dashboard.onrender.com/).

## Requirements
- Python 3.7+
- Required libraries: `pandas`, `plotly`, `seaborn`, `matplotlib`, `dash`, `dash-bootstrap-components`, `geopandas`

## Setting up
1. Clone the repository:
    ```bash
    git clone https://github.com/snobbybrat9/un-dashboard.git
    cd un-dashboard
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Uncomment the following line** in the `app.py` script:
    ```python
    # if __name__ == "__main__":
    #     app.run_server(debug=True)
    ```

3. Add the datasets to the `cleaned_datasets` directory.

## Usage
1. Run the app:
    ```bash
    python app.py
    ```

2. Open your browser and go to `http://127.0.0.1:8050/`.

## Project Structure
```plaintext
un-dashboard/
├── assets/
│   └── UN_logo.jpeg         # UN logo used in the sidebar
├── cleaned_datasets/        # Place your datasets here
├── Procfile                 # Required to run the dashboard on Render
├── app.py                   # Main application code
├── requirements.txt         # Required libraries
└── README.md                # This readme file
```
## About
Created by Gopesh Khanna
