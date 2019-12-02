import downloader

import time
import random
# '58606884048','58479215586','59227940223','70041567546','110459873908',
#                 '68743384278','58520849715','93711052684','67704411527','70486969147',
#                 '58673738672','58698814553','59902229872','58633239048', '56709647970'
user_id_list = []
for user_id in user_id_list:
    downloader.DouyinVideoDownloader(download_flag=True).\
        run(user_id=user_id,type_flag='p',watermark_flag=0,save_dir='../videos/douyin-get/')
    time.sleep(random.uniform(3,9))
    # downloader.DouyinVideoDownloader(download_flag=True).\
    #     run(user_id=user_id,type_flag='p',watermark_flag=1,save_dir='/Users/handsomechief/PycharmProjects3/vedios/douyin-mark/')
    # time.sleep(random.uniform(3,9))
    # downloader.DouyinVideoDownloader(download_flag=True).\
    #     run(user_id=user_id,type_flag='f',watermark_flag=0,save_dir='../vedios/douyin-get/')
    # time.sleep(random.uniform(3,9))
    # downloader.DouyinVideoDownloader(download_flag=True).\
    #     run(user_id=user_id,type_flag='f',watermark_flag=1,save_dir='/Users/handsomechief/PycharmProjects3/vedios/douyin-mark/')
    # time.sleep(random.uniform(3,9))


