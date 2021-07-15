import scrapy
import json
from hot.myproject.items import MyprojectItem
class UserSpider(scrapy.Spider):
    name = 'user'
    def start_requests(self):
    #获取不同页面响应数据
        # allowed_domains = ['pstat?mid=672328094&jsonp=jsonp']
        url = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=%s'
        for i in range(1,21):
            yield scrapy.Request(url%str(i), callback=self.parse)
    #解析每页热门视频mid
    def parse(self,response):
        info=response.json()
        mids=[]
        for i in range(0,20):
            # print(info['data']['list'][i]['tname'])
            mids.append(info['data']['list'][i]['owner']['mid'])
        for mid in mids:
            url='https://api.bilibili.com/x/relation/stat?vmid='+str(mid)+'&jsonp=json'
            yield scrapy.Request(url,callback=self.parse_)
    #解析粉丝、关注、mid
    def parse_(self, response):
        # cookie = {
        #     "buvid3=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; rpdid=|(RlRk||lYk0J'ul~|)|l|Jk; LIVE_BUVID=AUTO1215817316842516; CURRENT_FNVAL=80; _uuid=EDBDE4EB-AD65-AEE4-5633-09FC70232C0904562infoc; buivd_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; balh_is_closed=; balh_server_inner=__custom__; buvid_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; fingerprint3=06575671fef0d32400ca8fc17ec0c1a1; blackside_state=1; fingerprint_s=bb474829113b63fba96274751570c517; sid=hw4k0grb; DedeUserID=410282523; DedeUserID__ckMd5=0f009d0a30b0f8dc; CURRENT_BLACKGAP=1; CURRENT_QUALITY=80; fingerprint=193a958f170cd56ea90a9977b535b801; buvid_fp_plain=11ADC416-B239-4E90-915C-54F0AE5B7787155842infoc; SESSDATA=6b506635,1641628093,f4dd9*71; bili_jct=146f3423988132782f8f46b6d956b2c7; PVID=4; bp_t_offset_410282523=546841283443906465; bp_video_offset_410282523=546850972893330118; bfe_id=6f285c892d9d3c1f8f020adad8bed553"
        #
        # }
        headers = {
            'Cookie': "buvid3=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; rpdid=|(RlRk||lYk0J'ul~|)|l|Jk; LIVE_BUVID=AUTO1215817316842516; CURRENT_FNVAL=80; _uuid=EDBDE4EB-AD65-AEE4-5633-09FC70232C0904562infoc; buivd_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; balh_is_closed=; balh_server_inner=__custom__; buvid_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; fingerprint3=06575671fef0d32400ca8fc17ec0c1a1; blackside_state=1; fingerprint_s=bb474829113b63fba96274751570c517; sid=hw4k0grb; DedeUserID=410282523; DedeUserID__ckMd5=0f009d0a30b0f8dc; CURRENT_BLACKGAP=1; CURRENT_QUALITY=80; fingerprint=193a958f170cd56ea90a9977b535b801; buvid_fp_plain=11ADC416-B239-4E90-915C-54F0AE5B7787155842infoc; SESSDATA=6b506635,1641628093,f4dd9*71; bili_jct=146f3423988132782f8f46b6d956b2c7; PVID=4; bp_t_offset_410282523=546841283443906465; bp_video_offset_410282523=546850972893330118; bfe_id=6f285c892d9d3c1f8f020adad8bed553",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }
        info = response.json()
        item = MyprojectItem()
        follower=info['data']['follower']
        following=info['data']['following']
        mid=info['data']['mid']
        print('粉丝量:',follower,'关注数:',following,'Mid:',mid)
        item['follower']=follower
        item['following']=following
        item['mid']=mid
        new_url='https://api.bilibili.com/x/space/upstat?mid='+str(mid)+'&jsonp=jsonp'
        yield scrapy.Request(new_url,callback=self.parse__,headers=headers,meta={'item':item})
    #解析播放、阅读、喜欢
    def parse__(self,response):
        headers = {
            'Cookie': "buvid3=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; rpdid=|(RlRk||lYk0J'ul~|)|l|Jk; LIVE_BUVID=AUTO1215817316842516; CURRENT_FNVAL=80; _uuid=EDBDE4EB-AD65-AEE4-5633-09FC70232C0904562infoc; buivd_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; balh_is_closed=; balh_server_inner=__custom__; buvid_fp=140B48D3-650C-4F42-A12F-CF7821D927F1155821infoc; fingerprint3=06575671fef0d32400ca8fc17ec0c1a1; blackside_state=1; fingerprint_s=bb474829113b63fba96274751570c517; sid=hw4k0grb; DedeUserID=410282523; DedeUserID__ckMd5=0f009d0a30b0f8dc; CURRENT_BLACKGAP=1; CURRENT_QUALITY=80; fingerprint=193a958f170cd56ea90a9977b535b801; buvid_fp_plain=11ADC416-B239-4E90-915C-54F0AE5B7787155842infoc; SESSDATA=6b506635,1641628093,f4dd9*71; bili_jct=146f3423988132782f8f46b6d956b2c7; PVID=4; bp_t_offset_410282523=546841283443906465; bp_video_offset_410282523=546850972893330118; bfe_id=6f285c892d9d3c1f8f020adad8bed553",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }
        info =response.json()
        play_view=info['data']['archive']['view']
        read_view=info['data']['article']['view']
        likes=info['data']['likes']
        print('播放量:',play_view,'阅读数:',read_view,'喜欢:',likes)
        item = response.meta['item']
        item['play_view']=play_view
        item['read_view'] =read_view
        item['likes'] =likes
        mid = response.meta['item']['mid']
        new_url='https://api.bilibili.com/x/space/acc/info?mid='+str(mid)+'&jsonp=jsonp'
        yield scrapy.Request(new_url, callback=self.parse___, headers=headers,meta={'item':item})
    #解析名字、头像、签名
    def parse___(self,response):
        item = response.meta['item']
        info =response.json()
        name=info['data']['name']
        face=info['data']['face']
        sign=info['data']['sign']
        item['name'] =name
        item['face'] =face
        item['sign'] =sign
        print('名字:',name,'头像:',face,'签名:',sign)
        yield item


