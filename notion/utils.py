import requests, os
    
def get_file_url_list(page_header):
    file_url_list = []
    file_name_list = []
    for block in page_header:
        if block['type']=='file': 
            file_url = block['file']['file']['url']
            file_name = block['file']['name']
            file_url_list.append(file_url)
            file_name_list.append(file_name)
    return file_name_list, file_url_list
    
def get_image_url_list(page):
    file_url_list = []
    for block in page:
        if block['type']=='image': 
            file_url = block['image']['file']['url']
            file_url_list.append(file_url)
    return file_url_list

def download_file(file_name, file_url, outdir):
    response = requests.get(file_url)
    if response.status_code == 200:
        outpath = os.path.join(outdir, file_name)
        with open(outpath, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully!")
    else:
        print(f"Failed to download file: {response.status_code}")
    return outpath

def download_files(file_name_list, file_url_list, outdir):
    outpaths = []
    for file_name, file_url in zip(file_name_list, file_url_list):
        outpath = download_file(file_name, file_url, outdir)
        outpaths.append(outpath)
    return outpaths

def get_page_id(page_header): 
    page_url = page_header['url']
    page_id = page_url.split('/')[-1].split('-')[-1]
    # page_url = f'https://api.notion.com/v1/pages/{page_id}'
    return page_id