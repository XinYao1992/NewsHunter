import json


with open("selected_corpus/health_news.json") as data_file:
    data = json.load(data_file)

dic = {}
for key, value in data.iteritems():
    news = {}
    news["section"]=value["section"]
    news["title"]=value["title"]
    news["abstract"]=value["abstract"]
    news["url"]=value["url"]
    news["content"]=value["content"]
    news["byline"]=value["byline"]
    news["thumbnail_standard"]=value["thumbnail_standard"]
    news["source"]=value["source"]
    news["published_date"]=value["published_date"]
    news["des_facet"]=value["des_facet"]
    news["geo_facet"]=value["geo_facet"]
    dic[key] = news

with open("health2.json", 'w') as df:
    json.dump(dic, df)
