import os
import json
import shutil
import sqlite3
import platform
from pathlib import Path
from datetime import datetime

class BrowserDataCollector:
    def __init__(self):
        self.user_data_path = str(Path.home())
        self.output_folder = "browser_data_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(self.output_folder, exist_ok=True)
        
    def get_chrome_history(self):
        return self.get_browser_data(
            browser="Chrome",
            db_name="History",
            profile_path=os.path.join(
                self.user_data_path,
                'AppData', 'Local', 'Google', 'Chrome', 'User Data'
            ),
            history_query="""
                SELECT url, title, last_visit_time, visit_count 
                FROM urls ORDER BY last_visit_time DESC LIMIT 1000
            """
        )
    
    def get_chrome_autofill(self):
        return self.get_browser_data(
            browser="Chrome",
            db_name="Web Data",
            profile_path=os.path.join(
                self.user_data_path,
                'AppData', 'Local', 'Google', 'Chrome', 'User Data'
            ),
            autofill_query="""
                SELECT name, value FROM autofill ORDER BY date_last_used DESC LIMIT 1000
            """
        )
    
    def get_edge_history(self):
        return self.get_browser_data(
            browser="Edge",
            db_name="History",
            profile_path=os.path.join(
                self.user_data_path,
                'AppData', 'Local', 'Microsoft', 'Edge', 'User Data'
            ),
            history_query="""
                SELECT url, title, last_visit_time, visit_count 
                FROM urls ORDER BY last_visit_time DESC LIMIT 1000
            """
        )
    
    def get_edge_autofill(self):
        return self.get_browser_data(
            browser="Edge",
            db_name="Web Data",
            profile_path=os.path.join(
                self.user_data_path,
                'AppData', 'Local', 'Microsoft', 'Edge', 'User Data'
            ),
            autofill_query="""
                SELECT name, value FROM autofill ORDER BY date_last_used DESC LIMIT 1000
            """
        )
    
    def get_firefox_history(self):
        firefox_path = os.path.join(
            self.user_data_path,
            'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'
        )
        
        if not os.path.exists(firefox_path):
            return {"error": "Firefox profile directory not found"}
        
        profiles = [d for d in os.listdir(firefox_path) if d.endswith('.default-release')]
        if not profiles:
            return {"error": "No Firefox profile found"}
        
        history_data = []
        for profile in profiles:
            places_path = os.path.join(firefox_path, profile, 'places.sqlite')
            temp_path = os.path.join(self.output_folder, f'{profile}_firefox_history.db')
            
            try:
                shutil.copy2(places_path, temp_path)
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT url, title, last_visit_date, visit_count 
                    FROM moz_places ORDER BY last_visit_date DESC LIMIT 1000
                """)
                
                for row in cursor.fetchall():
                    history_data.append({
                        "url": row[0],
                        "title": row[1],
                        "last_visit": row[2],
                        "visit_count": row[3]
                    })
                
                conn.close()
                os.remove(temp_path)
            except (sqlite3.Error, FileNotFoundError) as e:
                return {"error": f"Error accessing Firefox data: {str(e)}"}
        
        return history_data

    def get_browser_data(self, browser, db_name, profile_path, history_query=None, autofill_query=None):
        profile_folders = [d for d in os.listdir(profile_path) if os.path.isdir(os.path.join(profile_path, d))]
        browser_data = {}

        for profile in profile_folders:
            db_path = os.path.join(profile_path, profile, db_name)
            temp_path = os.path.join(self.output_folder, f'{profile}_{db_name}.db')
            
            if not os.path.exists(db_path):
                continue
            
            shutil.copy2(db_path, temp_path)
            
            try:
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                # Ensure the profile key exists in browser_data
                if profile not in browser_data:
                    browser_data[profile] = {}

                if history_query:
                    cursor.execute(history_query)
                    browser_data[profile]["history"] = [{
                        "url": row[0],
                        "title": row[1],
                        "last_visit": row[2],
                        "visit_count": row[3]
                    } for row in cursor.fetchall()]
                
                if autofill_query:
                    cursor.execute(autofill_query)
                    browser_data[profile]["autofill"] = [{
                        "name": row[0],
                        "value": row[1]
                    } for row in cursor.fetchall()]
                
                conn.close()
                os.remove(temp_path)
            
            except sqlite3.Error as e:
                browser_data[profile] = {"error": f"SQLite error: {str(e)}"}
        
        return browser_data

    # def collect_all_data(self):
    #     data = {
    #         "system_info": {
    #             "platform": platform.platform(),
    #             "machine": platform.machine(),
    #             "processor": platform.processor(),
    #             "collection_time": datetime.now().isoformat()
    #         },
    #         "browsers": {
    #             "chrome": {
    #                 "history": self.get_chrome_history(),
    #                 "autofill": self.get_chrome_autofill()
    #             },
    #             "firefox": {
    #                 "history": self.get_firefox_history()
    #             },
    #             "edge": {
    #                 "history": self.get_edge_history(),
    #                 "autofill": self.get_edge_autofill()
    #             }
    #         }
    #     }
        
    #     # Save to JSON file per browser
    #     for browser, browser_data in data["browsers"].items():
    #         output_file = os.path.join(self.output_folder, f'{browser}_data.json')
    #         with open(output_file, 'w', encoding='utf-8') as f:
    #             json.dump({browser: browser_data}, f, indent=4, ensure_ascii=False)
        
    #     return self.output_folder
    
    def collect_all_data(self):
        data = {
            "chrome": self.get_chrome_history(),
            "firefox": self.get_firefox_history(),
            "edge": self.get_edge_history()
        }

        # Save data to the central database
        for browser, content in data.items():
            self.save_to_database(browser, "history", content)

if __name__ == "__main__":
    collector = BrowserDataCollector()
    output_folder = collector.collect_all_data()
    print(f"Data collected and saved in folder: {output_folder}")
