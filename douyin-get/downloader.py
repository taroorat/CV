# -*- coding: utf-8 -*-
# @Time    : 2019/9/17 14:25
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : downloader.py
# @Software: PyCharm

from contextlib import closing
import requests, json, re, os, sys
from urllib.parse import urlencode
import execjs
from ipaddress import ip_address
import random
import Util


class DouyinVideoDownloader:

    def __init__(self, user_id=None, watermark_flag=None, type_flag=None, download_flag=False):
        """
        抖音 App 视频下载
        """
        self.user_id = user_id
        self.watermark_flag = watermark_flag
        self.type_flag = type_flag
        self.download_flag = download_flag
        self.session = requests.session()
        with open('get_signature_douyin.js', 'rb') as f:
            self.js = f.read().decode()

    @staticmethod
    def get_random_proxy(url):
        while True:
            try:
                resp = requests.get('http://*************/random/')  # 代理池地址, 替换成自己的代理
                if url.startswith('https'):
                    proxy = resp.content.decode('utf-8')
                    proxies = {
                        'https': 'https://{}'.format(proxy)
                    }
                    return proxies
                elif url.startswith('http'):
                    proxy = resp.content.decode('utf-8')
                    proxies = {
                        'http': 'http://{}'.format(proxy)
                    }
                    return proxies
                else:
                    raise Exception('请检查协议头是否正确! ')
            except Exception as e:
                print('获取代理失败: ', e.args)

    def _set_session(self):
        """
        配置代理
        :return:
        """
        proxies = self.get_random_proxy('https')
        self.session.proxies.update(proxies)
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
            'X-Real-IP': str(proxies['https'].split('@')[1]).split(':')[0],
            'X-Forwarded-For': str(proxies['https'].split('@')[1]).split(':')[0],
        }

    def _fack_ip(self):
        """
        伪装 ip 代理
        :return:
        """
        rip = ip_address('0.0.0.0')
        while rip.is_private:
            rip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
            'X-Real-IP': str(rip),
            'X-Forwarded-For': str(rip),
        }

    def _get_tac(self, user_id):
        """
        个人主页获取 dytk、 tac 等关键参数
        :param user_id:
        :return:
        """
        share_user_url = 'https://www.douyin.com/share/user/%s' % user_id
        while True:
            try:
                # self._set_session()
                self._fack_ip()
                resp = self.session.get(share_user_url, timeout=30)
                while resp.status_code != 200:
                    resp = self.session.get(share_user_url)
                break
            except:
                pass
        sec_uid = ''  # 可以为空
        _dytk_re = re.compile(r"dytk\s*:\s*'(.+)'")
        dytk = _dytk_re.search(resp.text).group(1)
        _nickname_re = re.compile(r'<p class="nickname">(.+?)<\/p>')
        nickname = _nickname_re.search(resp.text).group(1)
        _tac_re = re.compile(r"tac='(.*?),<8~z")
        tac = _tac_re.search(resp.text).group(1)
        return sec_uid, dytk, nickname, tac

    def _update_tac(self, tac):
        """
        更新本地 js 全局变量 tac
        :param tac:
        :return:
        """
        _js_tac = re.search(r"var tac = '(.*?)' \+", self.js, re.S).group(0)
        return self.js.replace(_js_tac, "var tac = '" + tac + "' +")

    @staticmethod
    def _get_signature(user_id, js):
        ctx = execjs.compile(js)
        return ctx.call('generateSignature', user_id)

    def _format_api(self, user_id, max_cursor, type_flag='p'):
        """
        构造用户视频信息 api
        :return:
        """
        sec_uid, dytk, nickname, tac = self._get_tac(user_id)
        js = self._update_tac(tac)
        _signature = self._get_signature(user_id, js)
        params = {
            'user_id': user_id,
            'sec_uid': sec_uid,
            'count': '21',
            'max_cursor': max_cursor,
            'aid': '1128',
            '_signature': _signature,
            'dytk': dytk
        }
        base_api = 'https://www.douyin.com/aweme/v1/aweme/favorite' if type_flag == 'f' else 'https://www.douyin.com/aweme/v1/aweme/post'
        return base_api + '?' + urlencode(params), nickname

    def get_video_urls(self, user_id, type_flag='p'):
        """
        获取视频播放地址
        :param user_id: 用户 ID
        :return:
        """
        video_names = []
        video_urls = []
        share_urls = []
        nickname = ''
        max_cursor = 0
        result = {'aweme_list': [1]}
        i = 0
        page = 1
        has_more = True
        print('解析视频链接中...')
        while has_more and result['aweme_list'] != []:
            user_api, nickname = self._format_api(user_id, max_cursor, type_flag)
            try:
                resp = self.session.get(user_api, timeout=30)
                while resp.status_code != 200:
                    resp = self.session.get(user_api, timeout=30)
                result = json.loads(resp.text)
            except:
                pass
            while 'max_cursor' not in set(result.keys()):
                i = i + 1
                print('第{}次重新连接...'.format(i))
                # user_api = self.format_api(user_id, max_cursor, type_flag)
                # 每请求连接 100 次更换 IP
                if i % 100 == 0:
                    user_api, nickname = self._format_api(user_id, max_cursor, type_flag)
                try:
                    response = self.session.get(user_api, timeout=30)
                    while response.status_code != 200:
                        response = self.session.get(user_api, timeout=30)
                    result = json.loads(response.text)
                except:
                    pass
            i = 0
            for each in result['aweme_list']:
                try:
                    url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&line=0&ratio=720p&media_type=4&vr_type=0&test_cdn=None&improve_bitrate=0'
                    uri = each['video']['play_addr']['uri']
                    video_url = url % uri
                except:
                    continue
                share_desc = each['share_info']['share_desc']
                if os.name == 'nt':
                    for c in r'\/:*?"<>|':
                        nickname = nickname.replace(c, '').strip().strip('\.')
                        share_desc = share_desc.replace(c, '').strip()
                share_id = each['aweme_id']
                if share_desc in {'抖音-原创音乐短视频社区', 'TikTok', ''}:
                    video_names.append(share_id + '.mp4')
                else:
                    video_names.append(share_id + '-' + share_desc + '.mp4')
                share_urls.append(each['share_info']['share_url'])
                print(video_url)
                video_urls.append(video_url)
            print('成功获取第{}页视频地址! '.format(page))
            page += 1
            max_cursor = result.get('max_cursor', 0)
            has_more = result['has_more']

        return video_names, video_urls, share_urls, nickname

    @staticmethod
    def get_download_url(video_url, watermark_flag):
        """
        去水印
        :param video_url: 视频地址
        :param watermark_flag: 是否需要去水印
        :return:
        """
        # 带水印视频
        if watermark_flag:
            download_url = video_url.replace('/play/', '/playwm/')
        # 无水印视频
        else:
            download_url = video_url.replace('/playwm/', '/play/')

        return download_url

    def video_downloader(self, video_url, video_name, watermark_flag=False):
        """
        视频下载
        :param video_url: 视频地址
        :param video_name: 视频名称
        :param watermark_flag: 是否去水印
        :return:
        """
        size = 0
        video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
        # 模拟 APP 请求
        headers = {
            'user-agent': 'okhttp/3.10.0.1'
        }
        with closing(requests.get(video_url, headers=headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(video_name, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

                        sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()

    def run(self,user_id,type_flag,watermark_flag,save_dir):
        """
        运行函数
        """
        print(user_id,type_flag,watermark_flag,save_dir)
        if not self.user_id:
            self.user_id = user_id
            print(user_id)
        if not self.watermark_flag:
            self.watermark_flag = bool(int(watermark_flag))
        if not self.type_flag:
            self.type_flag = type_flag

        video_names, video_urls, share_urls, nickname = self.get_video_urls(self.user_id, self.type_flag)
        if not self.download_flag:
            return {
                'nickname': nickname,
                'data': [{video_names[i]: video_urls[i]} for i in range(len(video_names))]
            }
        nickname_dir = os.path.join(save_dir, nickname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if nickname not in os.listdir(save_dir):
            os.mkdir(nickname_dir)
        if self.type_flag == 'f':
            if 'favorite' not in os.listdir(nickname_dir):
                os.mkdir(os.path.join(nickname_dir, 'favorite'))
        print('视频下载中: 共有%d个作品!\n' % len(video_urls))
        for num in range(len(video_urls)):
            print('  下载第%d个视频链接 [%s] 中，请稍后!\n' % (num + 1, share_urls[num]))
            if '\\' in video_names[num]:
                video_name = video_names[num].replace('\\', '')
            elif '/' in video_names[num]:
                video_name = video_names[num].replace('/', '')
            else:
                video_name = video_names[num]
            video_path = os.path.join(nickname_dir, video_name) if self.type_flag != 'f' else os.path.join(
                nickname_dir, 'favorite', video_name)
            if os.path.isfile(video_path):
                print('视频已存在')
            else:
                self.video_downloader(video_urls[num], video_path, self.watermark_flag)
            print('\n')
        print('下载完成!')
