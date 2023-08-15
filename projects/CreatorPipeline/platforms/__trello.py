import requests

class TrelloBoard:
    """Trello Board Interface"""
    def __init__(self, board_id, api_key, api_token):
        self.board_id = board_id
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = 'https://api.trello.com/1'
        
    def get_lists(self):
        """Returns the lists for the board."""
        url = f"{self.base_url}/boards/{self.board_id}/lists"
        response = requests.get(url, params={'key': self.api_key, 'token': self.api_token})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")
    
    def add_card(self, list_id, name):
        """Adds a card to the list."""
        url = f"{self.base_url}/cards"
        response = requests.post(url, params={'key': self.api_key, 'token': self.api_token},
                                 json={'idList': list_id, 'name': name})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")
        
    def move_card(self, card_id, list_id):
        """Moves a card to a list."""
        url = f"{self.base_url}/cards/{card_id}"
        response = requests.put(url, params={'key': self.api_key, 'token': self.api_token},
                                json={'idList': list_id})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")
    
    def edit_card(self, card_id, name):
        """Edits a card."""
        url = f"{self.base_url}/cards/{card_id}"
        response = requests.put(url, params={'key': self.api_key, 'token': self.api_token},
                                json={'name': name})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")



###
board_id = 'your_board_id'
api_key = 'your_api_key'
api_token = 'your_api_token'

board = TrelloBoard(board_id, api_key, api_token)


