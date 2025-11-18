from pathlib import Path
from os import listdir
from typing import Any
from json import load
from typing import Dict

class DatabaseLocal:
    def __init__(self):
        self.defaultusers_path = Path('../local/default_profiles.json')
        self.database = listdir('app/local')


    def show_all_collections(self):
        return self.database
    
    def get_default_users(self, results: int | None = None):
        resultsData = []
        with open('app/local/default_profiles.json', 'r') as f:
            data: Dict = load(f)
        if not results:  
            return data
        results = int(results)
        for i in range(len(data)):
            if i == results:
                return resultsData
            resultsData.append(data[i])