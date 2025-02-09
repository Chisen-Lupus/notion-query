import requests, json, os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

class Query():

    __NOTION_TOKEN = None
    __headers = None

    DATABASE_ID = None
    PAGE_ID = None

    def __init__(self, token=None): 
        if token: 
            self.set_token(token)

    def set_token(self, token):
        self.__NOTION_TOKEN = token
        self.__headers = {
            "Authorization": "Bearer " + self.__NOTION_TOKEN,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    @staticmethod
    def is_page_selected(page, filters):
        """
        Check if a page matches the selection criteria.
        Args:
            page (dict): The page data containing properties.
            criteria (dict): The selection criteria with keys as property names and values as the expected value.
        Returns:
            bool: True if the page matches all criteria, False otherwise.
        """
        for key, expected_value in filters.items():
            prop = page['properties'].get(key)
            if not prop:
                return False
            if prop['type']=='select' and prop['select']['name']!=expected_value:
                return False
            if prop['type']=='status' and prop['status']['name']!=expected_value:
                return False
        return True

    @staticmethod
    def is_block_selected(block, filters):
        for key, expected_value in filters.items():
            prop = block.get(key)
            if not prop:
                return False
            if key=='type' and prop!=expected_value:
                return False
        return True

    def get_pages(self, num_pages=None, database_id=None, filters=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        DATABASE_ID = database_id if database_id else self.DATABASE_ID
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        get_all = num_pages is None
        page_size = 10000 if get_all else num_pages
        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.__headers)
        if response.status_code == 200:
            data = response.json()
            results = data["results"]
            if filters: 
                results = [page for page in results if self.is_page_selected(page, filters)]
            return results
        else:
            print(f"Failed to retrieve page content: {response.status_code}")
            print(response.text)  
            return
            
        # while data["has_more"] and get_all:
        #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        #     response = requests.post(url, json=payload, headers=self.__headers)
        #     data = response.json()
        #     results.extend(data["results"])
    
    def get_blocks(self, page_id=None, filters=None):
        PAGE_ID = page_id if page_id else self.PAGE_ID
        children_url = f'https://api.notion.com/v1/blocks/{PAGE_ID}/children'
        response = requests.get(children_url, headers=self.__headers)
        if response.status_code == 200:
            content_data = response.json()
            # print(json.dumps(content_data, indent=4))  # Pretty-print the page content
            results = content_data['results']
            if filters: 
                results = [block for block in results if self.is_block_selected(block, filters)]
            return results
        else:
            print(f"Failed to retrieve page content: {response.status_code}")
            print(response.text) 
            return






# TODO: 增量备份??
# IDEA: 搞个file explorer出来??