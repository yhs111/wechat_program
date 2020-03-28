from flask import Flask
from flask import jsonify, request
from models import UserInfo


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # 支持中文


@app.route('/main/getnewslist/<name>')
def index(name):
    lst = []
    user_info = UserInfo()
    data = user_info.get_users(name)
    for item in data:
        dic = dict()
        dic["img_url"] = item["img_url"]
        dic["title"] = item["title"]
        dic["aut_name"] = item["aut_name"]
        dic["nid"] = str(item["_id"])  # object id
        desc = ",".join(item["materials"].keys())
        dic["desc"] = desc[:25] + '...' if len(desc) > 25 else desc  # 描述
        lst.append(dic)
    return jsonify(lst)

@app.route('/main/GetNewsById')
def detail():
    user_info = UserInfo()
    nid = request.args.get("nid")
    data = user_info.get_user(nid)
    data["_id"] = nid
    return jsonify(data)

@app.route('/main/searchList')
def search():
    lst = []
    user_info = UserInfo()
    string = request.args.get("string")
    data = user_info.get_search_result(string)
    for item in data:
        dic = dict()
        dic["img_url"] = item["img_url"]
        dic["title"] = item["title"]
        dic["aut_name"] = item["aut_name"]
        dic["nid"] = str(item["_id"])  # object id
        desc = ",".join(item["materials"].keys())
        dic["desc"] = desc[:25] + '...' if len(desc) > 25 else desc  # 描述
        lst.append(dic)
    return jsonify(lst)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=44313)
