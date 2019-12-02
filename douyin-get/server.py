# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 21:42
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : server.py
# @Software: PyCharm


from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer
from downloader import DouyinVideoDownloader

__all__ = ['app']

app = Flask(__name__)


def main(address="0.0.0.0", port=8778):
    http_server = WSGIServer((address, port), app)
    http_server.serve_forever()


@app.route('/')
def root():
    return '<h2>Douyin Video Downloader</h2>'


@app.route('/get_videos/<user_id>/<has_watermark>/<v_type>')
def get_videos(user_id, has_watermark, v_type):
    """
    获取用户视频下载地址
    :param user_id: 用户ID
    :param has_watermark: 是否视频水印
    :param v_type: 视频类型： f -> 收藏的, p -> 上传到额
    :return:
    """
    result = DouyinVideoDownloader(user_id, has_watermark, v_type).run()
    if isinstance(request, dict):
        return jsonify({
            'code': 1,
            'message': 'success',
            'data': result
        })
    return jsonify({
        'code': 0,
        'message': 'fail',
        'data': None
    })


if __name__ == '__main__':
    main()
