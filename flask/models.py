import pymongo
import time
from settings import DB_MONGO, URL
from bson import ObjectId


class UserInfo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(DB_MONGO["host"], DB_MONGO["port"])
        self.db = self.client["toutiao"]
        self.user = self.db.user_info
        self.index = self.db.user_id

    # def save(self, *args, **kwargs):
    #     uid = self.user.insert(kwargs)
    #     return uid

    def get_users(self, name):
        user_infos = []
        users = self.user.find({"classify": name})
        for user in users:
            if not user.get("img_url"):
                user["img_url"] = URL
            user_infos.append(user)
        return user_infos

    def get_user(self, uid):
        user = self.user.find_one({"_id": ObjectId(uid)})
        if not user.get("img_url"):
            user["img_url"] = URL

        # 前期数据爬取考虑不周这里转换格式, 适用于小程序构建表格
        lst = []
        for key, value in user["materials"].items():
            lst.append({"key": key, "value": value})
        user['materials'] = lst

        # 做法
        step_list = []
        for n, item in enumerate(user["step"], 1):
            dic = dict()
            dic["index"] = n
            dic["url"] = item[0]
            dic["desc"] = item[1]
            step_list.append(dic)
        user['step'] = step_list
        return user

    def get_search_result(self, string):
        # 正则匹配实现类似 like 模糊查询
        users = self.user.find({"$or": [{"classify": {"$regex": string}}, {"title": {"$regex": string}}]})
        lst = []
        for user in users:
            if not user.get("img_url"):
                user["img_url"] = URL
            lst.append(user)
        return lst


if __name__ == "__main__":
    user = UserInfo()
    news_list = [
        {
            "id": 1,
            "headUrl": "../../resource/images/UserHeaders/user1.jpg",
            "imageUrls": [],
            "isFocus": True,
            "isVideo": True,
            "newsText": "",
            "newsTitle": "只争朝夕，不负韶华",
            "userName": "YHS",
            "newsAbstrack": None,
            "isOriginal": True,
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "videoUrl": "http://wxsnsdy.tc.qq.com/105/20210/snsdyvideodownload?filekey=30280201010421301f0201690402534804102ca905ce620b1241b726bc41dcff44e00204012882540400&bizid=1023&hy=SH&fileparam=302c020101042530230204136ffd93020457e3c4ff02024ef202031e8d7f02030f42400204045a320a0201000400"
        },
        {
            "id": 2,
            "headUrl": "../../resource/images/UserHeaders/user1.jpg",
            "imageUrls": ["../resource/images/NewsImages/news1.jpg",],
            "isFocus": True,
            "isVideo": False,
            "newsText": "<p><span>[特朗普：希望中国购买美国生产的喷气发动机 国家安全不是“挡箭牌”]</span><span>格隆汇2月19日丨特朗普政府此前考虑阻止通用电气公司向中国出口LEAP-1C航空发动机。不过，特朗普最新表示，周二拒绝了美国国会提出的一些对中国贸易的限制，他说，“美国国家安全”不可以被当作给那些与美国进行贸易的国家制造麻烦的借口。特朗普在推特写道：“美国不可以也不会变成一个让那些计划购买美国商品的国家难以打交道的国家，包括永远也不会以美国国家安全为借口在内，否则，我们的企业为了保存竞争力，就会被迫离开美国。”同时他在推特补充说：“譬如，我希望中国购买我们的喷气式发动机，世界上最好的喷气式发动机。”</span></p><image src='../../resource/images/NewsImages/news1.jpg' alt=''/>",
            "newsTitle": "特朗普：希望中国购买美国生产的喷气发动机",
            "userName": "YHS",
            "newsAbstrack": None,
            "isOriginal": True,
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "videoUrl": None,
        }
    ]
    for new in news_list:
        user.save(**new)
    # print(user.get_users())
    print(user.get_user(1))
