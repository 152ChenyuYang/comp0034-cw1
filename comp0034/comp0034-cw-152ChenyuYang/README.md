1.Introduction
This project is a housing supply and demand visualization system developed based on Dash, which is used to analyze and display housing supply and waiting list data.
Main functions include:
1. Line chart: Display housing waiting list trends in different regions
2. Bar chart: Display housing supply
3. Map: Visualize housing supply distribution in various regions
4. Pie chart: Display housing distribution ratio in different regions
5. Interactive function: Select region and data type in the drop-down menu, and dynamically update visualization


2.Structure
│── data0035/coursework1
│   ├── database
│   │   ├── local_authority_housing.db  # SQLite Database
│   ├── output
│   ├── __init__.py
│   ├── affordable.py   # Housing data processing
│   ├── database.py     # Connecting to a database
│   ├── waiting_list.py # Processing waiting list data
│
├── section1
│   ├── app.py   # Dash application main file
│   ├── fix_geo_data.py  # Working with geographic data
│   ├── generate_geo_data.py  # Generate geographic data
│   ├── geo_locations.csv  # Geographic coordinate data
│
├── section2
│   ├── test.py  # Pytest Automated UI Testing
│
├── requirements.txt  
├── README.md  


3.
# Enter the project directory
cd C:\Users\YANG\Desktop\comp0034\comp0034-cw-152ChenyuYang

# Create a virtual environment (only need to be executed once)
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate

# Install Python dependencies required for the project
pip install -r requirements.txt

# Run `generate_geo_date.py`
python section1/generate_geo_data.py

# Run `fix_geo_date.py`
python section1/fix_geo_data.py

# Run `app.py`
python section1/app.py
You will get 
Dash is running on http://127.0.0.1:5050/

 * Serving Flask app 'app'
 * Debug mode: on

# Run `test.py`
pytest section2/test.py
