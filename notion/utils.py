import requests, os
from dateutil import parser
    
def get_file_urls(page_header):
    file_urls = []
    file_names = []
    for block in page_header:
        if block['type']=='file': 
            file_url = block['file']['file']['url']
            file_name = block['file']['name']
            file_urls.append(file_url)
            file_names.append(file_name)
    return file_names, file_urls
    
def get_image_urls(page):
    file_urls = []
    for block in page:
        if block['type']=='image': 
            file_url = block['image']['file']['url']
            file_urls.append(file_url)
    return file_urls

def download_file(file_name, file_url, outdir, verbose=True):
    response = requests.get(file_url)
    if response.status_code == 200:
        outpath = os.path.join(outdir, file_name)
        with open(outpath, "wb") as file:
            file.write(response.content)
        if verbose: print(f"File '{file_name}' downloaded successfully!")
    else:
        if verbose: print(f"Failed to download file: {response.status_code}")
    return outpath

def download_files(file_names, file_urls, outdir, verbose=True):
    outpaths = []
    for file_name, file_url in zip(file_names, file_urls):
        outpath = download_file(file_name, file_url, outdir, verbose)
        outpaths.append(outpath)
    return outpaths

def get_page_id(page_header): 
    page_url = page_header['url']
    page_id = page_url.split('/')[-1].split('-')[-1]
    # page_url = f'https://api.notion.com/v1/pages/{page_id}'
    return page_id

def get_page_title(page_header, name_property='Name'):
    page_title = page_header['properties'][name_property]['title'][0]['plain_text']
    return page_title

def get_block_times(blocks):
    last_edited_times = [parser.parse(block['last_edited_time']) for block in blocks]
    return last_edited_times

def get_url_extensions(urls):
    extensions = [url.split('?')[0].split('.')[-1] for url in urls]
    return extensions