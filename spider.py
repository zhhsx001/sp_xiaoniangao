import requests
import uuid
import logging
import random
import time
from qiniu import Auth
from qiniu.services.storage.bucket import BucketManager
import models
import input_sql

logger = logging.getLogger('ArtPub')

LOG_DIR = '/data/zongqinhui/logs/'
PROGRAM = 'ArtPub'
PACKAGE = 'FamilyAs'

class Spider(object):
    def __init__(self):
        self.content = {}
        self.title_list = []
        self.v_list = []
        self.proxies = None
        self.headers = {
            'charset': "utf-8",
            'accept-encoding': "gzip",
            'referer': "https://servicewechat.com/wxd7911e4c177690e4/317/page-frame.html",
            'content-type': "application/json",
            'uuid': "26631558-5aa5-4997-9706-2c81a5326676",
            'user-agent': "Mozilla/5.0 (Linux; Android 8.1.0; M1816 Build/O11019; wv) AppleWebKit/537.36 (KHTML,"
                          " like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 MicroMessenger/"
                          "7.0.8.1540(0x27000833) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64",
            'content-length': "946",
            'host': "kapi.xiaoniangao.cn",
            'connection': "Keep-Alive",
            'cache-control': "no-cache",
        }
        self.access_key = 'j0gcZOz9MBPPiNfMZG4Kh1JqjR9OJKwXvLXAMuuT'
        self.secret_key = '5y6ROW7__THnTYTWDxVowEI4R1A27p1dRs9E8lhP'
        self.bucket_name = 'kingmashortvideo'

    def uuid_and_UA(self):
        # data 和 user-agent 有关
        yekai = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-G9730 Build/PPR1.180610.011; wv) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 '
                               'MicroMessenger/7.0.6.1480(0x2700063C) Process/appbrand0 NetType/WIFI Language/zh_CN',
                'uuid': '901f5f43-1d0d-47f9-98f8-fa8ae1c55130', }
        zhanghua = {'uuid': "26631558-5aa5-4997-9706-2c81a5326676",
        'user-agent': "Mozilla/5.0 (Linux; Android 8.1.0; M1816 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like "
                      "Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 MicroMessenger/7.0.8.1540"
                      "(0x27000833) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64",
        }

    def make_proxy(self):
        # 在服务器上运行proxy程序。使用web api调用
        # 暂时不需要。
        pass

    def spider_list(self):
        url = "https://kapi.xiaoniangao.cn/trends/get_recommend_trends"

        data = "{\"rec_ab_config\":{\"ban_ab\":1,\"city_slot\":0,\"multi_ab\":1,\"region_ab\":{\"num\":4," \
               "\"position\":{\"0\":1,\"1\":2,\"2\":3,\"3\":4}}},\"log_params\":{\"page\":\"discover_rec\"," \
               "\"common\":{\"os\":\"Android 8.1.0\",\"device\":\"M1816\",\"weixinver\":\"7.0.8\"," \
               "\"srcver\":\"2.9.3\"}},\"log_common_params\":{\"e\":[{\"data\":{\"topic\":\"recommend\"," \
               "\"page\":\"discoverIndexPage\"}}],\"ext\":{\"os\":\"Android 8.1.0\",\"device\":\"M1816\"," \
               "\"weixinver\":\"7.0.8\",\"srcver\":\"2.9.3\"}}," \
               "\"qs\":\"imageMogr2/gravity/center/rotate/$/thumbnail/!750x500r/crop/750x500/interlace/1/format/jpg" \
               "\",\"h_qs\":\"imageMogr2/gravity/center/rotate/$/thumbnail/!80x80r/crop/80x80/interlace/1/format/jpg" \
               "\",\"share_width\":625,\"share_height\":500,\"ext\":{\"items\":{\"12952717\":{\"type\":\"rec\"," \
               "\"pd\":93.727,\"ct\":1573722505531,\"ut\":1573722608047},\"15136629\":{\"type\":\"rec\"," \
               "\"pd\":10.359,\"ct\":1573723795368,\"ut\":1573723813153}}}," \
               "\"token\":\"620ae6a48e8432a82fb102be427b53af\",\"uid\":\"26631558-5aa5-4997-9706-2c81a5326676\"," \
               "\"proj\":\"ma\",\"wx_ver\":\"7.0.8\",\"code_ver\":\"1.45.5\"} "
        try:
            response = requests.request("POST", url, data=data, headers=self.headers, proxies=self.proxies)
            self.content = response.json()
        except Exception as e:
            logger.error('spider vedio list failed')

    def analysis_list(self):
        try:
            for v_text in self.content['data']['list']:
                self.title_list.append(v_text['title'])
                self.v_list.append(v_text['v_url'])
        except Exception as e:
            logger.error('video list analysis failed: ', e)

    def qiniu_fetch_vedio(self, v_url, key=None):
        qiniuAuth = Auth(self.access_key, self.secret_key)
        bucket_ = BucketManager(qiniuAuth)
        if not key:
            key = str(uuid.uuid4()).replace('-', '')
        res, info = bucket_.fetch(v_url, self.bucket_name, key=key)
        return res, info

    def qiniu_upload_vedio(self):
        # 配合proxy进行ip代理后下载视频，然后上传。
        pass

    def grab(self, video_type=0):
        # 视频入库并抓取
        list = self.v_list

        try:
            for temp in list:
                if random.randint(1, 100) > 57:
                    continue
                video = models.VideoXng()
                video.album_id = temp['album_id']
                video.title = temp['title']
                video.producer = temp['user']['nick']
                video.url = temp['url']
                video.v_url = temp['v_url']
                video.hurl = temp['user']['hurl']
                video.views = temp['views']
                video.cover_watermark = temp['cover_watermark']
                video.total = temp['favor']['total']
                video.comment_count = temp['comment_count']
                video.du = temp['du']
                video.type = video_type
                self.qiniu_fetch_vedio(temp['v_url'])
                time.sleep(random.randint(4*60, 6*60))
            logger.info("grab success%s", video_type)
        except Exception as e:
            logger.error("grab error%s-%s", video_type, e)

    def download_video(self):
        headers = {
            'connection': "keep-alive",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/78.0.3904.97 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;v=b3",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
            'cache-control': "no-cache",
        }
        for i, v_url in enumerate(self.v_list):
            try:
                res = requests.get(v_url, headers=headers)
                with open('%d_video.mp4' % i, 'wb') as f:
                    f.write(res.content)
                if i == 0:
                    break
            except Exception as e:
                logger.error("download_video failed video, video url: %s" % v_url, e)

    def simulate(self):
        # 使用时间任务控制器，模拟人类行为
        pass


if __name__ == "__main__":
    config = {
        'SQLALCHEMY_DATABASE_URI': 'xiaoniangao',
        'SQLALCHEMY_POOL_TIMEOUT': 2,
        'SQLALCHEMY_POOL_SIZE': 3,
        'SQLALCHEMY_POOL_RECYCLE': 4,
    }
    input_sql.init_db(config)
    case = Spider()
    case.spider_list()
    case.analysis_list()
    for v in case.v_list:
        print(v)
    case.grab()