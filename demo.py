# -*- coding: utf-8 -*-
from xiamiclient import XiamiClient


if __name__ == '__main__':
    XIAMI_CLIENT = XiamiClient()

    # 搜索功能
    print('search:')
    print(XIAMI_CLIENT.search(u'珊瑚海', limit=2))

    # 查看详情
    ret = XIAMI_CLIENT.get_detail(1774955492)
    print('detail:')
    print(ret)

    # 每个音频的location,每天中国区时间0点更新
    # 这个location可以转化为src,在第二天中国区时间8点过期
    # 拿到了src,就可以下载音乐或者用于自己的在线服务了
    print('finally get the src:')
    print(XIAMI_CLIENT.parse_location(ret['location']))
