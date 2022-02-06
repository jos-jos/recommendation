import sys
import requests
import json
import os
import cfg

def huawei_nlp(argv, model):
    max_len = 2
    while (len(argv) < max_len):
        argv.append(None)
    endpoint = "nlp-ext.cn-north-4.myhuaweicloud.com"
    project_id = "07e9fe35b400108a2f25c004c2d26d9d"
    #华为提供的基本的权限，免费的
    model_body = {
        # 根据指定文本，抽取其中最能够反映文本主题或者意思的词汇。
        "keyword-extraction": {'text': argv[0], 'limit': argv[1], 'lang': 'zh'},
        # 对文本进行命名实体识别分析，目前支持人名、地名、时间、组织机构类实体的识别。
        "ner": {'text': argv[0], 'lang': 'zh'},
        "text-similarity/advance": {'text1': argv[0], 'text2': argv[1], 'lang': 'zh'},
    }

    url = 'https://%s/v1/%s/nlp-fundamental/%s'%(endpoint, project_id, list(model_body.keys())[model])  # endpoint和project_id需替换
    token = cfg.config["X-Subject-Token"]
    header = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }
    
    resp = requests.post(url, data=json.dumps(model_body[list(model_body.keys())[model]]), headers=header)

    text_dir =json.loads(resp.text)
    return text_dir

def getToken(name, passwd):
    url = "https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens"
    header = {
        'Content-Type': 'application/json',
    }
    body = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": name,
                        "password": passwd,
                        "domain": {
                            "name":name 
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": "cn-north-4"
                }
            }
        }
    }
    resp = requests.post(url, data=json.dumps(body), headers=header)
    with open(os.path.join(sys.path[0], "cfg.py"), "w") as f:
        f.write("config = %s"%(str(resp.headers)))
    print(resp.headers)

if __name__ == '__main__':
    # getToken("PreviousLetters", "Zhishui197063")
    inputs = ['华为技术有限公司成立于1987年，总部位于广东省深圳市龙岗区。华为是全球领先的信息与通信技术（ICT）解决方案供应商，专注于ICT领域，坚持稳健经营、持续创新、开放合作，在电信运营商、企业、终端和云计算等领域构筑了端到端的解决方案优势，为运营商客户、企业客户和消费者提供有竞争力的ICT解决方案、产品和服务，并致力于实现未来信息社会、构建更美好的全联接世界。', 8]
    temp = huawei_nlp(inputs, 0)
    temp = temp['words']
    print(temp)

    # inputs = ['昨天程序员李小明来到北京参加开发者大赛，在比赛中表现优异，赢得了第一名。']
    # temp = huawei_nlp(inputs, 1)
    # temp = temp["named_entities"]
    # print(temp)

    inputs = ["杭州有啥好玩的", "杭州哪里好玩"]
    inputs = ["我熟悉Javascript特性", "我擅长Javascript编程"]
    inputs = ["我熟悉Javascript特性", "我熟悉Java特性"]
    temp = huawei_nlp(inputs, 2)
    temp = temp["similarity"]
    print(temp)
