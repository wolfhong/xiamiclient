# -*- coding: utf-8 -*-
from xiamiclient import XiamiClient
import pprint


if __name__ == '__main__':
    XIAMI_CLIENT = XiamiClient()

    # 搜索功能
    print('search:')
    search_list = XIAMI_CLIENT.search(u'珊瑚海', limit=2)
    print(search_list)

    # 查看详情
    ret = XIAMI_CLIENT.get_detail(search_list[0]['id'])
    print('detail:')
    print(pprint.pformat(ret))

    # get_detail方法中返回的信息,song_url是根据其对应的location字段计算而来的;
    # location/song_url 每天中国区时间0点更新,在第二天中国区时间8点过期
    # 拿到了song_url,就可以下载音乐或者用于自己的在线服务
    # location转化为song_url的方式如下:
    print('how location be parsed to song_url:')
    print(XIAMI_CLIENT.parse_location(ret['location']))

    # 查看专辑
    song_list = XIAMI_CLIENT.get_album(ret['album_id'])
    print("album:")
    print(pprint.pformat(song_list))
