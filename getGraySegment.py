import requests
import os,base64,time

def getSeg(dir_path,file_path):
    srcfile=dir_path+'/'+file_path
    print(srcfile)
    resfile='resimgs/'+srcfile[-10:]
    print(resfile)
    if resfile[8:] not in os.listdir('resimgs/'):

        print(2, resfile[8:] )
        url='https://api-cn.faceplusplus.com/humanbodypp/v2/segment'
        d = {"api_key":"UjmoCBhB3Jpmtbgc2MxpT8c3LjuZ5NwC",
             "api_secret": "q0qPbyhW4vlWyQoe_zH1pcJTmW_edu_Z",
             "return_grayscale":2}
        files = {"image_file": open(srcfile, "rb")}
        try:

            response = requests.post(url, data=d, files=files)
            req_dict = response.json()
            imgdata = base64.b64decode(req_dict['result'])
            print(imgdata)
            with open(resfile,'wb') as f:
                f.write(imgdata)

        except Exception as e:
            print(e)
    else:
        print(1)

if __name__ =='__main__':
    dir = 'images/dance/'
    print(len(os.listdir(dir)))
    print(len(os.listdir('resimgs/')))
    while (len(os.listdir(dir)) != len(os.listdir('resimgs/'))):
        for i in os.listdir(dir):
            getSeg(dir,i)
        time.sleep(3)