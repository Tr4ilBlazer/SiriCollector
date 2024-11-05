Browser Data Collector
This script, BrowserDataCollector, extracts and saves browsing data from Chrome, Firefox, and Edge browsers on Windows. The data includes history and autofill information, making it useful for analyzing browsing patterns or backing up browser data.

Features
Extract Browser Data: Supports Chrome, Firefox, and Edge. Retrieves:
History: URLs visited, titles, visit counts, and last visit times.
Autofill (Chrome and Edge only): Autofill names and values.
Data Export: Saves data to JSON files or a centralized SQLite database.
Cross-Browser Support: Automatically detects installed browser profiles and retrieves data accordingly.
Prerequisites
Python 3.x: Ensure Python is installed on your machine.
Operating System: Windows (uses Windows-specific paths for browser data).
Installation
Clone or Download this repository.
Navigate to the project directory.
Install dependencies (only standard libraries are used, so no installations are required).
For custom installations, create and activate a virtual environment (optional):

bash
Copy code
python -m venv env
source env/bin/activate  # For MacOS/Linux
env\Scripts\activate     # For Windows
Install the required libraries:
bash
Copy code
pip install -r requirements.txt
Usage
Initialization:

Initialize the script by creating a BrowserDataCollector instance. This automatically sets up a timestamped output directory for storing collected data.
Data Collection:

Use collect_all_data() to gather history data across supported browsers and save it into a central database.
Output:

The output directory will be named browser_data_YYYYMMDD_HHMMSS with a timestamp of the current date and time.
Each browser's data will be saved in JSON files, such as chrome_data.json, firefox_data.json, and edge_data.json.
Example
To run the script, use the following command:

python
Copy code
python script_name.py
Upon execution, the script will print the location of the output directory.

Methods
get_chrome_history()
Retrieves Chrome browsing history.

get_chrome_autofill()
Retrieves Chrome autofill data.

get_edge_history()
Retrieves Edge browsing history.

get_edge_autofill()
Retrieves Edge autofill data.

get_firefox_history()
Retrieves Firefox browsing history.

get_browser_data(browser, db_name, profile_path, history_query=None, autofill_query=None)
Handles database operations for extracting history or autofill data from the specified browser and profile.

collect_all_data()
Collects browsing history for all supported browsers and saves it into the output folder.

Error Handling
If a browser or profile folder is not found, or if there are errors accessing the data files, the script will log an error message and continue processing other browsers.

