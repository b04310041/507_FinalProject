import sys
import requests
from bs4 import BeautifulSoup

###CPBL 比賽場館鄰近景點

import json

CACHE_FILENAME = "site.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict



def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

BASEBALL_CACHE = open_cache()



def cache_spot(url):
    url_city = url
    if url_city in BASEBALL_CACHE:
        return BASEBALL_CACHE[url_city]
    else:
        spot(url)
        save_cache(BASEBALL_CACHE)
        return BASEBALL_CACHE[url_city]
    


def spot(url):

    lst = []
    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')

    for aaa in soup.findAll('li',{'id':'Search_Content_li'}):
        h3=aaa.findAll("h3")
        site=h3[0]
        lst.append(site.text)
    
    url_city = url
    BASEBALL_CACHE[url_city] = lst
    return BASEBALL_CACHE[url_city]
    

### scrape sites in Taipei
url_Taipei = "https://okgo.tw/Search.html?kw=%25E5%258F%25B0%25E5%258C%2597%25E5%25B8%2582%25E5%25A4%25A7%25E5%25AE%2589%25E5%258D%2580&st=1"

### scrape sites in new_taipei_city

url_new_taipei_city="https://okgo.tw/Search.html?kw=%25E6%2596%25B0%25E5%258C%2597%25E5%25B8%2582%25E6%2596%25B0%25E8%258E%258A%25E5%258D%2580&st=1#"


### scrape sites in Taoyuan
url_Taoyuan = "https://okgo.tw/Search.html?kw=%25E6%25A1%2583%25E5%259C%2592%25E5%25B8%2582%25E6%25A1%2583%25E5%259C%2592%25E5%258D%2580&st=1"



### scrape sites in Hsinchu
url_Hsinchu = 'https://okgo.tw/Search.html?kw=%25E6%2596%25B0%25E7%25AB%25B9%25E7%25B8%25A3%25E7%25AB%25B9%25E5%258C%2597%25E5%25B8%2582&st=1'



### scrape sites in Taichung
url_Taichung = 'https://okgo.tw/Search.html?kw=%25E5%258F%25B0%25E4%25B8%25AD%25E5%25B8%2582%25E5%258C%2597%25E5%25B1%25AF%25E5%258D%2580&st=1'



### scrape sites in Kaohsiung
url_Kaohsiung = 'https://okgo.tw/Search.html?kw=%25E9%25AB%2598%25E9%259B%2584%25E5%25B8%2582%25E9%25B3%25B3%25E5%25B1%25B1%25E5%258D%2580&st=1'




city = {
    "臺北和平籃球館": "Taipei",
    "新北市立新莊體育館": "new_taipei_city",
    "桃園市立綜合體育館": "Taoyuan",
    "新竹縣體育館": "Hsinchu",
    "臺中洲際迷你蛋": "Taichung",
    "臺中洲際迷你蛋": "Taichung",
    "高雄市鳳山體育館": "Kaohsiung"
}



address = {"Taipei": "台灣台北市大安區敦南街76巷28號",
            "new_taipei_city": "新北市新莊區和興街66號",
            "Taoyuan": "桃園市中壢區領航北路一段1號",
            "Hsinchu": "台灣新竹縣竹北市福興東路一段197號",
            "Taichung": "台中市北屯區崇德路三段835號",
            "Kaohsiung": "台灣高雄市鳳山區體育路65號"}

"""
list_Taipei = ['大安森林公園', '自來水園區', '蒙藏文物展示中心', '清真寺']
list_new_taipei_city = ['新莊文昌祠', '輔仁大學', '廣福宮(三山國王廟)', '新泰公園', '青年公園', '新莊武聖廟', '臺北縣立新莊體育場', '慈祐宮', '塭仔底溼地公園', '新莊中港大排親水步道']
list_Taoyuan = ['奧爾(Owl) 森林學堂', '三民公園(三民運動公園)', '虎頭山公園', '桃園親子館(原桃園三民遊客服務中心)', '第一河濱公園', '土地公文化館', '風禾公園滾輪溜滑梯']
list_Hsinchu = ['新月沙灣（坎頂與坎仔腳）', '蓮花寺', '新瓦屋客家文化園區（忠孝堂）', '溝貝親子休閒農莊', '竹北濱海遊憩區', '頭前溪豆腐岩', '問禮堂', '采田福地', '新竹縣立體育館', '拔子窟自行車道', '台灣高鐵探索館（第二代）']
list_Taichung = ['浪漫情人橋', '大坑登山步道', '大坑8號步道', '大坑9號步道', '中正露營區', '大坑5號步道', '大坑6號步道', '台中民俗公園', '崇德觀光玉市', '米笠休閒莊園(原荔園休閒農場)', '大坑4號步道', '舊社公園', '藍天白雲橋', '八二三紀念公園', '天津成衣街', '梅川公園', '大坑2號步道', '大坑1號步道', '敦化公園', '大坑3號步道']
list_Kaohsiung = ['國父紀念館（已拆除）', '大東文化藝術中心', '衛武營都會公園', '鳳儀書院', '打鐵街', '澄瀾砲台', '慈恩紀念圖書館', '平成砲台', '訓風砲台', '東便門（東福橋）', '開漳聖王廟', '曹公廟', '龍山寺', '高雄市立圖書館．曹公分館', '城隍廟', '雙慈亭']
"""

"""
allsite = {'Taipei': spot(url_Taipei), 
            'new_taipei_city': spot(url_new_taipei_city) , 
            'Taoyuan': spot(url_Taoyuan),
            'Hsinchu': spot(url_Hsinchu),
            'Taichung': spot(url_Taichung),
            'Kaohsiung': spot(url_Kaohsiung)}

"""


print(cache_spot(url_Taipei))