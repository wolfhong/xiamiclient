## Why use xiamiclient?
前团队有个服务,是点歌电台,希望集成虾米音乐;但目前虾米音乐和淘宝并不提供相关API(可能曾经提供过,但是后来关闭了,总之当时就是没能找到官方途径来对接虾米)。

于是，自己写了一套符合自己需求的虾米音乐API:

- 搜索(可获取音乐的ID)
- 查看详情(根据ID)
- 获取音乐资源文件(该音乐文件的地址需要根据location进行转化得到,并且有效时间只有一天,在第二天的中国区时间8点过期,每天的中国区时间0点更新)


## Installtion
- clone the code and enter the folder
- python install setup.py
- or you can directly place the code into your project.


## Example

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


## More
如果有其他需求,将会继续提供更多的API.当然啦,官方API一旦开放,本项目将废弃TT


## A story TT
点歌电台上线后,有用户通过搜索点了一首声优的访谈节目音频,也不知道怎么搜索到的,导致一首歌占用了超过1小时的时长TT.
所以对于搜索结果的使用,最好根据需求来判断时长(detail接口提供),过短和过长的文件都应该拒绝.
