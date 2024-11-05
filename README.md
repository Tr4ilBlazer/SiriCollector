
---

# 🧭 Browser Data Collector

`BrowserDataCollector` is a Python-based tool for extracting and saving browsing data from **Chrome**, **Firefox**, and **Edge** browsers on Windows. The tool collects browsing history and autofill information, making it valuable for backing up browser data or conducting data analysis.

---

## ✨ Features

- **Browser Data Extraction**: Supports Chrome, Firefox, and Edge, collecting:
  - **History**: URLs, titles, visit counts, and last visit times.
  - **Autofill (Chrome and Edge)**: Autofill names and values.
- **Data Export**: Saves extracted data to JSON files or a centralized SQLite database.
- **Cross-Browser Support**: Automatically detects installed profiles and gathers data from each.

## 🛠 Prerequisites

- **Python 3.x**: Ensure Python is installed on your machine.
- **Operating System**: Windows (uses Windows-specific paths for browser data).
  
## 📦 Installation

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/yourusername/BrowserDataCollector.git
   cd BrowserDataCollector
   ```

2. **Create and Activate** a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate      # MacOS/Linux
   env\Scripts\activate         # Windows
   ```

3. **Install Requirements**: Run the following command to install any required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   > **Note**: No external libraries are required as the script uses Python's standard library. If dependencies are added in the future, they will be listed in `requirements.txt`.

---

## 🚀 Usage

1. **Initialize**: Create a `BrowserDataCollector` instance to set up a timestamped output directory for data storage.
2. **Collect Data**: Use `collect_all_data()` to gather data across browsers and save it to a central database.
3. **Output**: Collected data is saved in an output directory named `browser_data_YYYYMMDD_HHMMSS`.

### 🔍 Example

Run the script with:
```bash
python script_name.py
```

After execution, the script will output the directory path where data has been saved.

---

## 📖 Method Overview

- ### `get_chrome_history()`
   Retrieves Chrome browsing history.

- ### `get_chrome_autofill()`
   Retrieves Chrome autofill data.

- ### `get_edge_history()`
   Retrieves Edge browsing history.

- ### `get_edge_autofill()`
   Retrieves Edge autofill data.

- ### `get_firefox_history()`
   Retrieves Firefox browsing history.

- ### `get_browser_data(browser, db_name, profile_path, history_query=None, autofill_query=None)`
   Handles database operations for extracting history or autofill data from the specified browser and profile.

- ### `collect_all_data()`
   Collects browsing history for all supported browsers and saves it into the output folder.

---

## 📂 Error Handling

If a browser or profile folder is not found, or if there are errors accessing data files, the script will log an error message and continue processing other browsers.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
