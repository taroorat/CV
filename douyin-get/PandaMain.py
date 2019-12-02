import downloader

import time
import random

user_id_list = ['100440255420','97010501953','74895660791','75987318416','82805151033','72373173288','63301606743','98873186680', '102777167489','96892812209']
for user_id in user_id_list:
    downloader.DouyinVideoDownloader(download_flag=True).run(user_id=user_id,type_flag='p',watermark_flag=0,save_dir='/Users/handsomechief/PycharmProjects3/vedios/douyin-get/panda/')
    time.sleep(random.uniform(3,9))
    downloader.DouyinVideoDownloader(download_flag=True).run(user_id=user_id,type_flag='p',watermark_flag=1,save_dir='/Users/handsomechief/PycharmProjects3/vedios/douyin-mark/panda/')
    time.sleep(random.uniform(3,9))

