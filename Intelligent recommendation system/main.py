import os
import sys
import json
import jieba
import numpy as np

import show
from utils import readJS
from tf_idf import Words
from nlp import huawei_nlp

def main_nlp_image():
    i = 0
    max_num = 10
    job_data = readJS("data/2021-10-19.json")
    while i < max_num:
        index = list(job_data.keys())[i]
        str_temp = job_data[index]["JobCategoryName"]
        text = [job_data[index]["JobDescription"], 10]
        result = nlp.huawei_nlp(text, 0)["words"]
        result.insert(0, str_temp)
        show.img_generate(result[:3], "%s.png"%(index))
        i += 1

class Resume:
    def __init__(self, json_name):
        self.data = readJS(json_name)
        self.basic = self.data["基本信息"]
        self.skill = self.data["技能"]
        self.learning = self.data["学习能力"]
        self.education = self.data["教育背景"]
        self.experience = self.data["工作经历"]
        self.certificate = self.data["证书"]
        
        self.target_job = self.basic["期望职位"]
        self.target_place = self.basic["工作地点"]
        self.target_salary = self.basic["期待薪资"]
        self.education_level = ["高中","不限","大专", "本科", "硕士", "博士"]  #0,1,2,3,4

        self.education_id = 1
        self.title_weight = 0.3
        self.jieba_weight = 1-self.title_weight

        self.march = []
        self.march_place = []
        self.march_salary = []
        self.march_nothing = []
    
    def preprocess(self):
        for index in range(len(self.education_level)):
            if self.education_level[index] in self.basic["学历"]:
                self.education_id = index
                break
        print(self.education_id)
        self.jieba = " ".join(list(jieba.cut("，".join(self.skill))))
    
    def title_sort(self, title, index_list):    #tf_idf 匹配
        inputs = []
        results = []
        inputs.append(self.target_job)
        inputs += title
        self.title_model = Words(inputs)
        similar = self.title_model.similarity()
        sorted_id = sorted(range(len(similar)), key=lambda k: similar[k], reverse=True)
        for index in sorted_id:
            results.append(index_list[index])
        return results
    
    def description_sort(self, description, index_list):   #匹配
        inputs = []
        results = []
        inputs.append(self.jieba)
        inputs += description
        self.description_model = Words(inputs)
        similar = self.description_model.similarity()
        sorted_id = sorted(range(len(similar)), key=lambda k: similar[k], reverse=True)
        for index in sorted_id:
            results.append(index_list[index])
        return results
    
    def demo_sort(self, job_dirt):
        title = []
        jieba = []
        results = []
        keys_list = list(job_dirt.keys())
        for key in keys_list:
            jieba.append(job_dirt[key]["jieba"])
            title.append(job_dirt[key]["job_title"])
        _ = self.title_sort(title, keys_list)
        _ = self.description_sort(jieba, keys_list)
        print(type(self.title_model.results))
        title_sim = np.array(self.title_model.results)*self.title_weight
        jieba_sim = np.array(self.description_model.results)*self.jieba_weight
        similar = list(title_sim + jieba_sim)
        sorted_id = sorted(range(len(similar)), key=lambda k: similar[k], reverse=True)
        for index in sorted_id:
            results.append(keys_list[index])
        for key in results:
            city_march = 0
            salary_march = 0
            if self.target_place in job_dirt[key]["workCity"] or job_dirt[key]["workCity"] in self.target_place:
                city_march = 1
            if int(self.target_salary) >= job_dirt[key]["salaryValue"][0] or job_dirt[key]["salaryValue"][0] == 0:
                salary_march = 1
            if city_march and salary_march:            
                self.march.append([key, job_dirt[key]])
            elif city_march:
                self.march_place.append([key, job_dirt[key]])
            elif salary_march:
                self.march_salary.append([key, job_dirt[key]])
            else:
                self.march_nothing.append([key, job_dirt[key]])
    
    def show(self):
        print("March city and salary")
        for i in self.march:
            print(i[0])
        print("March city")
        for i in self.march_place:
            print(i[0])
        print("March salary")
        for i in self.march_salary:
            print(i[0])
        print("March nothing")
        for i in self.march_nothing:
            print(i[0])


class Dataset:             #
    def __init__(self, json_name):
        self.org_name = json_name
        self.org_data = readJS(json_name)
        self.data = self.org_data
        self.key_words_num = 10
        self.education_pools = [[], [], [], [], [], []]
        self.education_level = ["高中", "不限", "大专", "本科", "硕士", "博士"]
        self.job_title = ["job_title", ["JobCategoryName", "JobSubCategoryName", "JobTitle"]]
    
    def set_education_pools(self):     #可保存
        for key in self.data.keys():
            self.education_pools[self.data[key]["education_id"]].append(key)
    
    def cut_dataset(self, begin, number):
        self.data = {}
        key_list = list(self.org_data.keys())
        for index in range(len(self.org_data)):
            if begin <= index < (begin + number):
                self.data[key_list[index]] = self.org_data[key_list[index]]
    
    def title_transform(self):
        for key in self.data.keys():
            find_level = 1
            self.data[key][self.job_title[0]] = " ".join([self.data[key][i] for i in self.job_title[1]])
            for index in range(len(self.education_level)):
                if self.education_level[index] in self.data[key]["education"]:
                    self.data[key]["education_id"] = index
                    find_level = 0
                    break
            if find_level:
                print(self.data[key]["education"])
                self.data[key]["education_id"] = 1
    
    def salary_value(self):
        for key in self.data.keys():
            self.data[key]["salaryValue"] = [int(i) for i in self.data[key]["salaryReal"].split("-")]
    
    def jieba_description(self):
        for key in self.data.keys():
            self.data[key]["jieba"] = " ".join(list(jieba.cut(self.data[key]["JobDescription"])))
    
    def huawei_nlp_keywords(self):    
        for key in self.data.keys():
            inputs = [self.data[key]["JobDescription"], self.key_words_num]
            self.data[key]["nlp_keywords"] = huawei_nlp(inputs, 0)['words']

    def get_list(self, key_name, education_index=10):
        results = []
        self.index_list = []
        for index in range(len(self.education_pools)):
            if index <= education_index:
                for key in self.education_pools[index]:
                    self.index_list.append(key)
                    results.append(self.data[key][key_name])
        return  results, self.index_list
    
    def get_dirt(self, education_index=10):
        results = {}
        for index in range(len(self.education_pools)):
            if index <= education_index:
                for key in self.education_pools[index]:
                    results[key] = self.data[key]
        return results
 
    def save(self):
        name = self.org_name.replace(".json", "-processed.json")
        js = json.dumps(self.data, indent=4, separators=(',', ':'), ensure_ascii=False)
        with open(name, "w", encoding="utf-8") as f:
            f.write(js)

if __name__ == "__main__":
    job_data = Dataset("data/2021-10-20.json")
    job_data.title_transform()
    job_data.set_education_pools()
    job_data.salary_value()
    job_data.jieba_description()
    job_data.save()
    aoshen = Resume("demo.json")
    aoshen.preprocess()
    '''
    job_title, index_list = job_data.get_list("job_title", education_index=aoshen.education_id)
    description, index_list = job_data.get_list("jieba", education_index=aoshen.education_id)
    print(aoshen.title_sort(job_title, index_list))
    print(aoshen.description_sort(description, index_list))
    '''

    job_dirt = job_data.get_dirt(education_index=aoshen.education_id)
    aoshen.demo_sort(job_dirt)   #可保存
    aoshen.show()
