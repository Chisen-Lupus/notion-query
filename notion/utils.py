import requests, os
    
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
