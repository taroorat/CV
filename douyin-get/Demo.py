

import requests, zipfile, os
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None
def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def unzip_file(file_name, unzip_path):
    zip_ref = zipfile.ZipFile(file_name, 'r')
    zip_ref.extractall(unzip_path)
    zip_ref.close()
    os.remove(file_name)

import os

file_id = '1rPcbnanuApZeo2uc7h55OneBkbcFCnnf'
chpt_path = './datasets/'
if not os.path.isdir(chpt_path):
    os.makedirs(chpt_path)
destination = os.path.join(chpt_path, 'datasets.zip')
download_file_from_google_drive(file_id, destination)
unzip_file(destination, chpt_path)


# import os
# import random
#
# def dir_path(path):
#
#     dir=random.choice(os.listdir(path))
#     while dir == '.DS_Store':
#         dir = random.choice(os.listdir(path))
#     dir_path = path + dir + '/'
#     return dir_path
#
#
# def file_path(path):
#
#     file=random.choice(os.listdir(path))
#     file_path = path + file + '/'
#     return file_path
#
#
# if __name__ == '__main__':
#     dir=dir_path('/Users/handsomechief/PycharmProjects3/vedios/douyin-get/')
#     file=file_path(dir)
#     print(file)
