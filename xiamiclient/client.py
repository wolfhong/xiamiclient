# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import logging
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import json
import requests
import traceback
try:
    from urllib import unquote
except ImportError:  # PY3
    from urllib.parse import unquote


class XiamiClient(object):

    def __init__(self, timeout=2, retry=1):
        self.timeout = timeout  # 单次请求超时
        self.retry = retry  # 重试次数

    def _http_url(self, method, url, data, retry=None):
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Referer': 'https://login.xiami.com/'
        }
        if retry is None:
            retry = self.retry  # 设置允许重试次数
        try:
            r = requests.get(url, params=data, timeout=self.timeout, headers=headers)
            if not 200 <= r.status_code < 300:
                raise AssertionError('not 200: %s' % r.status_code)
            return r
        except:
            if retry > 0:
                retry -= 1
                return self._http_url(method, url, data, retry=retry)
            else:
                raise

    def search(self, key, limit=30):
        '''
        @brief search song by keyword
        '''
        if not key:
            return []
        try:
            url = 'http://www.xiami.com/web/search-songs'
            data = {'key': key, 'limit': limit}
            r = self._http_url('get', url, data)
            ret_list = json.loads(r.text)
            assert isinstance(ret_list, (list, tuple))
            return ret_list
        except:
            logging.error(traceback.format_exc())
            return []

    def parse_location(self, _str):
        '''
        @brief 虾米音乐的音频文件有认证,每次认证只能访问一天,过期时间为中国区第二天8点.
               认证的authkey根据location字段进行组合,location每天0点更新.
               本函数将location转化为可供下载访问的文件地址.
        @param _str 音乐对象的location字段
        @return 文件地址
        '''
        head = int(_str[0])
        _str = _str[1:]
        rows = head
        cols = int(len(_str)/rows) + 1

        out = ""
        full_row = len(_str) % head
        for c in range(cols):
            for r in range(rows):
                if c == (cols - 1) and r >= full_row:
                    continue
                if r < full_row:
                    char = _str[r*cols+c]
                else:
                    char = _str[cols*full_row+(r-full_row)*(cols-1)+c]
                out += char
        return unquote(out).replace("^", "0")

    def _extract_song(self, track):
        ret = {}
        keep_list = [
            'songName', 'song_id', 'album_id', 'album_name', 'background',
            'artist', 'artist_url', 'lyric', 'location',
            'pic', 'album_pic', 'length', 'artist_id',
        ]
        for k in keep_list:
            element_list = track.getElementsByTagName(k)
            if len(element_list) > 0:
                ret[k] = element_list[0].firstChild.nodeValue
        if 'location' in ret:
            ret['song_url'] = self.parse_location(ret['location'])
        return ret

    def get_detail(self, _id):
        '''
        @brief 返回一首歌的详细信息
        @param _id 对象ID,在search接口中可以查看到
        @return dict
        '''
        try:
            url = 'http://www.xiami.com/song/playlist/id/%s' % _id
            r = self._http_url('get', url, {})
            doc = parseString(r.text.encode('utf8'))
            tracks = doc.getElementsByTagName("track")
            if len(tracks) > 0:
                return self._extract_song(tracks[0])
            return {}
        except:
            logging.error(traceback.format_exc())
            return {}

    def get_album(self, _id):
        '''
        @brief 返回专题中的所有歌曲信息
        @param _id albumID
        @return a list of song-dict
        '''
        try:
            url = 'http://www.xiami.com/song/playlist/id/%s/type/1' % _id
            r = self._http_url('get', url, {})
            doc = parseString(r.text.encode('utf8'))
            tracks = doc.getElementsByTagName("track")
            ret_list = []
            for index, item in enumerate(tracks):
                if len(item.childNodes) > 1:  # have dirty data
                    ret = self._extract_song(item)
                    ret_list.append(ret)
            return ret_list
        except:
            logging.error(traceback.format_exc())
            return []
