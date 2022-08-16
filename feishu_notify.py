import json
import requests

app_id=''
app_secret=''
receive_id=''

# receive_id  =  open_id \ user_id \ union_id \ email \ chat_id
# https://open.feishu.cn/document/home/user-identity-introduction/how-to-get

# content & msg_type  =  text \ post \ image \ interactive
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json#c9e08671

# Authorization = access token
# https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM#top_anchor

#获取 tenant_access_token（企业自建应用）
def get_tenant_access_token():
    url = "	https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {'Content-Type': 'application/json'}
    params = {"app_id":app_id,"app_secret": app_secret}
    response = requests.request("POST", url, params=params, headers=headers)
    token=json.loads(response.content)
    return token['tenant_access_token']

#获取chat_id
def get_chat_id():
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': 'Bearer '+get_tenant_access_token(),
        'Content-Type': 'application/json'}
    params = {"receive_id_type":"user_id"} 
    req = {
        "receive_id": receive_id,
        "content": json.dumps(text('get_chat_id')),
        "msg_type": "text",}
    response = requests.request("POST", url, params=params, headers=headers, data=json.dumps(req))
    chat=json.loads(response.content)
    return (chat['data']['chat_id'])

#获取会话（包括单聊、群组）的历史消息（聊天记录）
def get_chat_history():
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {'Authorization': 'Bearer '+get_tenant_access_token()}
    params = {"container_id_type":"chat","container_id":get_chat_id()} 
    response = requests.request("GET", url, params=params, headers=headers)
    return response.content

#文本
def text(t):
    return {"text":f"{t}"}

#富文本
def post():
    post={
	"zh_cn": {
		"title": "我是一个标题",
		"content": [
			[{
					"tag": "text",
					"text": "第一行 :"
				},
				{
					"tag": "a",
					"href": "http://www.feishu.cn",
					"text": "超链接"
				}
			],
			[{
				"tag": "img",
				"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
			}]
		]
	}
    }
    return post

#图片
def image():
    # Get image_key
    #https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
    return {"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"}

#消息卡片
def interactive(title,link,text):
    interactive={
        "elements": [
            {
            "tag": "markdown",
            "content": f"**[{title}]({link})**\n --------------\n{text}"
            }
        ]
    }
    return interactive

#分享群名片
def share_chat():
    return {"chat_id": "oc_0dd200d32fda15216d2c2ef1ddb32f76"}

#分享个人名片
def share_user():
    return {"user_id": "ou_0dd200d32fda15216d2c2ef1ddb32f76"}

#分享文件
def file():
    #通过上传文件获取文件key
    #https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg"}

#分享语音
def audio():
    #通过上传文件获取文件key
    #https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg"}

#分享视频
def audio():
    #通过上传文件获取文件 file_key
    #https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    #通过上传图片获取视频封面 image_key
    #https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg","image_key": "img_xxxxxx"}

def send(title,link,text):
    req = {"receive_id": receive_id,
           "content": json.dumps(interactive(title,link,text)),
           "msg_type": "interactive",}
    response = requests.request("POST","https://open.feishu.cn/open-apis/im/v1/messages",
                                params={"receive_id_type":"user_id"},
                                headers={'Authorization': 'Bearer '+get_tenant_access_token(),
                                         'Content-Type': 'application/json'},
                                data=json.dumps(req))
    #print(response.content)
    return response.content