from datetime import datetime

import requests
import json
import os

class PrizePicker:
    def __init__(self):
        self.upcoming_lines_url = 'https://api.dailyfantasyapi.io/v1/lines/upcoming'
        self.upcoming_games_url = 'https://api.dailyfantasyapi.io/v1/games/upcoming'
        self.key = self.load_api_key()

    def load_api_key(self):
        with open('key.txt', 'r') as f:
            return f.read().strip()

    def file_path(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        return f'{current_date}.json'

    def file_exists(self):
        path = self.file_path()
        return os.path.exists(path)

    def fetch_upcoming_games(self):
        headers = {
            'x-api-key': self.key
        }
        params = {
            'league': 'NBA'             # 'MLB' 'NFL' 'NBA' 'NHL' 'SOCCER'
        }

        try:
            response = requests.get(
                self.upcoming_games_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            print(f'API request successful. Status code: {response.status_code}')
            print()
            print(response.content)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {str(e)}')
            exit()

    def fetch_upcoming_lines(self):
        headers = {
            'x-api-key': self.key
        }
        params = {
            'sportsbook': 'PrizePicks', # 'PrizePicks' 'Underdog' 'ParlayPlay'
            'league': 'NBA'             # 'MLB' 'NFL' 'NBA' 'NHL' 'SOCCER'
        }

        try:
            response = requests.get(
                self.upcoming_lines_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            print(f'API request successful. Status code: {response.status_code}')
            print()
            print(response.content)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {str(e)}')
            exit()

    def save_json(self, data):
        path = self.file_path()
        try:
            print(f'Attempting to save data to {path}')
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
            if os.path.exists(path):
                file_size = os.path.getsize(path)
                print(f'Data saved successfully to {path} (size: {file_size} bytes)')
                return True
            else:
                print(f'File was not created at {path}')
                return False
            
        except Exception as e:
            print(f'Error saving data to {path}: {str(e)}')
            return False

    def run(self):
        path = self.file_path()
        
        if self.file_exists():
            refetch = input(f'{path} exists already, enter [Y] to re-fetch lines >')
            if refetch != 'Y':
                print('Exiting application...')
                exit()

        #data = self.fetch_upcoming_lines()
        data = self.fetch_upcoming_games()
        
        if self.save_json(data):
            print(f'Successfully saved new data to {path}')
        else:
            print('Failed to save data')
            

if __name__ == '__main__':
    picker = PrizePicker()
    picker.run()