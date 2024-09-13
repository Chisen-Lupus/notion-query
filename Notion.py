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

    def get_page_list(self, num_pages=None, database_id=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        DATABASE_ID = database_id if database_id else self.DATABASE_ID
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        get_all = num_pages is None
        page_size = 100 if get_all else num_pages
        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.__headers)
        data = response.json()
        results = data["results"]

        # while data["has_more"] and get_all:
        #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        #     response = requests.post(url, json=payload, headers=self.__headers)
        #     data = response.json()
        #     results.extend(data["results"])

        return results
    
    def get_block_list(self, page_id=None):
        PAGE_ID = page_id if page_id else self.PAGE_ID
        children_url = f'https://api.notion.com/v1/blocks/{PAGE_ID}/children'
        # Send the GET request to retrieve the page content (blocks)
        response = requests.get(children_url, headers=self.__headers)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            content_data = response.json()
            # print(json.dumps(content_data, indent=4))  # Pretty-print the page content
            return content_data
        else:
            print(f"Failed to retrieve page content: {response.status_code}")
            print(response.text)  # Print error details
            return
    
    def get_file_url_list(self, content_data):
        # TODO: generalize to all kinds of file
        file_url_list = []
        file_name_list = []
        for block in content_data['results']:
            if block['type']=='file': 
                file_url = block['file']['file']['url']
                file_name = block['file']['name']
                file_url_list.append(file_url)
                file_name_list.append(file_name)
        return file_name_list, file_url_list

    def download_files(self, file_name_list, file_url_list, outdir):
        outpaths = []
        for file_name, file_url in zip(file_name_list, file_url_list):
            # Send a GET request to download the file
            response = requests.get(file_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Write the content to a file
                outpath = os.path.join(outdir, file_name)
                with open(outpath, "wb") as file:
                    file.write(response.content)
                print("File downloaded successfully!")
                outpaths.append(outpath)
            else:
                print(f"Failed to download file: {response.status_code}")

        return outpaths

    @classmethod
    def display_single_image(cls, path):
        # Open the image using Pillow
        img = Image.open(path)

        # Display the image
        plt.imshow(img)
        plt.axis('off')  # Hide axes
        plt.show()

    @classmethod
    def display_multiple_images(cls, paths):
        img_count = len(paths)
        grid = int(np.ceil(np.sqrt(img_count)))
        fig, axs = plt.subplots(grid, grid)
        axs = axs.flat
        for i in range(len(axs)):
            if i<img_count:
                path = paths[i]
                img = Image.open(path)
                axs[i].imshow(img)
            axs[i].axis('off')  # Hide axes
        plt.tight_layout()
        plt.show()








# TODO: needs a image display function