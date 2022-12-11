import sys
import requests
from bs4 import BeautifulSoup

import googlemaps
from datetime import datetime
import time

from prettytable import PrettyTable
from final_tree import tree_reader

#################################################### CACHE ###################################################
##############################################################################################################


import json

CACHE_FILENAME = "cache.json"

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




########################################## SCRAPE GAME INFORMATION ###########################################
##############################################################################################################



# print(dict_date_game['01/08'])
# {'time': ['14:30', '17:00'], 'teams': ['Formosa Taishin Dreamers', 'Kaohsiung 17LIVE Steelers', ['Taipei Fubon Braves', 'Hsinchu Jko Lioneers']]}


"""
dict_date_game = {
    '12/01': {
        'time': ['17:00', '12:00'],
        'city': ['place1', 'place2'],
        'team': [['team1', 'team2'], [team C, team D]]
    },

    '12/05': {
        'time': [12:00],
        'city': ['place1', 'place2'],
        'team': [['team1', 'team2']]
    }
}

"""



def cache_game_info(url):
    if 'dict_date_game' in BASEBALL_CACHE:
        return BASEBALL_CACHE['dict_date_game']
    else:
        game_info(url)
        save_cache(BASEBALL_CACHE)
        return BASEBALL_CACHE['dict_date_game']


def game_info(url):

    dict_date_game = {}

    table_div_class = "bg-white text-dark border-bottom border-top matches"

    date_div_class = 'col-lg-1 col-12 text-center align-self-center match_row_datetime'
    date_h5_class = 'fs16 mt-2 mb-1'
    day_h5_class = 'fs12 mb-2'
    time_h5_class = 'fs12'
    row_div_class = "row mx-0"
    twoTeam_spam_class = "fs12 PC_only"
    city_h5_class = "fs12 mb-0"

    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')
    table = soup.find('div', {'class':'bg-white text-dark border-bottom border-top matches'})

    for row in table.find_all('div', {'class': row_div_class}):

        for div in row.find_all('div', {'class': date_div_class}):
            
            date = div.find('h5', {'class': date_h5_class}).text
            time = div.find('h6', {'class': time_h5_class}).text
            city = row.find('h5', {'class': city_h5_class}).text
            two_teams = row.find_all('span', {'class': twoTeam_spam_class})

            list_two_teams = []
            for i in two_teams:
                list_two_teams.append(i.text)


            if date in dict_date_game:
                dict = dict_date_game[date]
                
                list_time = dict['time']
                list_time.append(time)

                list_city = dict['city']
                list_city.append(city)

                list_teams = dict['teams']
                list_teams.append(list_two_teams)
                
            else:
                dict_date_game[date] = {}
                dict_date_game[date]['time'] = [time]
                dict_date_game[date]['city'] = [city]
                dict_date_game[date]['teams'] = []
                dict_date_game[date]['teams'].append(list_two_teams)
    BASEBALL_CACHE['dict_date_game'] = dict_date_game
    return BASEBALL_CACHE['dict_date_game']






######################################### SCRAPE TOURIST SPOTS ###############################################
##############################################################################################################




def cache_spot(url):
    """
    Return a list
    [spot1, spot2, spot3, spot4...]
    """
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
    


############################################## SCRAPE RESTAURANTS #############################################
##############################################################################################################



def cache_get_place_result(add):
    if 'add' in BASEBALL_CACHE:
        return BASEBALL_CACHE['add']
    else:
        get_place_result(add)
        save_cache(BASEBALL_CACHE)
        return BASEBALL_CACHE['add']

def get_place_result(address):

    gmaps = googlemaps.Client(key='AIzaSyANO8edIKpdIKabmw-IDY0ZFP5cvtSuKsU')

    geocode_result = gmaps.geocode(address)

    lat = geocode_result[0]['geometry']['location']['lat']
    lon = geocode_result[0]['geometry']['location']['lng']
    loc=(str(lat),str(lon))

    places_result = gmaps.places_nearby(location=loc,radius=1000,open_now=False,type='restaurant')
    BASEBALL_CACHE['add'] = places_result
    return BASEBALL_CACHE['add']



def get_all_restaurant_with_rating__ratingNumber_address(places_result):

    # print(get_all_restaurant_with_rating__ratingNumber_address(places_result)[19])
    # ['name', 4, 340, 'address']
    
    all = []
    for i in range(len(places_result["results"])):
        temp=[places_result['results'][i]["name"],places_result['results'][i]["rating"],places_result['results'][i]["user_ratings_total"],
                places_result['results'][i]["vicinity"]]
        all.append(temp)
    time.sleep(0.0001)

    try:
        places_result = gmaps.places_nearby(page_token = places_result['next_page_token'])
        for i in range(len(places_result["results"])):
            temp=[places_result['results'][i]["name"],places_result['results'][i]["rating"],places_result['results'][i]["user_ratings_total"],
                    places_result['results'][i]["vicinity"]]
            all.append(temp)
        time.sleep(0.0001)

    except:
        1+1

    try:
        places_result = gmaps.places_nearby(page_token = places_result['next_page_token'])   
        for i in range(len(places_result["results"])):
            temp=[places_result['results'][i]["name"],places_result['results'][i]["rating"],places_result['results'][i]["user_ratings_total"],
                places_result['results'][i]["vicinity"]]
            all.append(temp)
    except:
        1+1

    return all


"""
[[name, rating score, number of rating, address],
[name, rating score, number of rating, address],
[name, rating score, number of rating, address],
[name, rating score, number of rating, address],
[name, rating score, number of rating, address]

"""
def get_top_5_restaurant(all_restaurant):  

    #print(get_top_5_restaurant(all))

    top_5_restaurant = []

    #>50人評分
    morethanfiftyrating=[]
    for i in all:
        if i[2] > 49:
            morethanfiftyrating.append(i)
            

    #排序
    def sor(x):
        return(x[1])

    top5 = sorted(morethanfiftyrating, reverse=True, key=sor)

        
    if len(top5) < 5:
        top_5_restaurant = top5
    else:
        top_5_restaurant = []
        for i in top5:
            top_5_restaurant.append(i)
        top_5_restaurant = top_5_restaurant[0:5]
    return top_5_restaurant




############################################### USER INTERFACE ###############################################
##############################################################################################################


def printout(p):      
    
    x = PrettyTable()

    x.field_names = ["Date", "Time", "City", "Teams", "Site", "Restaurant","Address"]
    for i in range(l): # i = game1, game2
    
        # in case no more than 5 sites )
        if len(allsite[city_list[i]]) < 5:
            n = len(allsite[city_list[i]])
        else:
            n = 5
        
        # in case no more than 5 restaurants 
        if len(list_top_5[i]) < 5:
            if len(list_top_5[i]) < n:
                n = len(list_top_5[i])


        for j in range(n): # j = site1, restaurant1, ... site5, restaurant5 
            dict_game_atThatDay = dict_date_game[date]
            if j==0:                

                x.add_row([date,
                            dict_game_atThatDay['time'][i], 
                            city_list[i], 
                            dict_game_atThatDay['teams'][i][0]+" vs "+dict_game_atThatDay['teams'][i][1], 
                            allsite[city_list[i]][j], 
                            "("+str(list_top_5[i][j][1])+")"+str(list_top_5[i][j][0]),
                            list_top_5[i][j][3]])
            else:
                x.add_row(["",
                            "", 
                            "", 
                            "", 
                            allsite[city_list[i]][j],
                            "("+str(list_top_5[i][j][1])+")"+str(list_top_5[i][j][0]),
                            list_top_5[i][j][3]])
                
    x.align = 'l'
    x._max_width = {"Address " : 50}
    print(x)



############################################### URL & DATA ###################################################
##############################################################################################################


# scrape game information
url = 'https://pleagueofficial.com/schedule-regular-season'
dict_date_game = cache_game_info(url)

#sceape spots
### Taipei
url_Taipei = "https://okgo.tw/Search.html?kw=%25E5%258F%25B0%25E5%258C%2597%25E5%25B8%2582%25E5%25A4%25A7%25E5%25AE%2589%25E5%258D%2580&st=1"

### new_taipei_city
url_new_taipei_city="https://okgo.tw/Search.html?kw=%25E6%2596%25B0%25E5%258C%2597%25E5%25B8%2582%25E6%2596%25B0%25E8%258E%258A%25E5%258D%2580&st=1#"

### Taoyuan
url_Taoyuan = "https://okgo.tw/Search.html?kw=%25E6%25A1%2583%25E5%259C%2592%25E5%25B8%2582%25E6%25A1%2583%25E5%259C%2592%25E5%258D%2580&st=1"

###  Hsinchu
url_Hsinchu = 'https://okgo.tw/Search.html?kw=%25E6%2596%25B0%25E7%25AB%25B9%25E7%25B8%25A3%25E7%25AB%25B9%25E5%258C%2597%25E5%25B8%2582&st=1'

### Taichung
url_Taichung = 'https://okgo.tw/Search.html?kw=%25E5%258F%25B0%25E4%25B8%25AD%25E5%25B8%2582%25E5%258C%2597%25E5%25B1%25AF%25E5%258D%2580&st=1'

### Kaohsiung
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


# scrape sites from cities
allsite = {'Taipei': cache_spot(url_Taipei), 
            'new_taipei_city': cache_spot(url_new_taipei_city) , 
            'Taoyuan': cache_spot(url_Taoyuan),
            'Hsinchu': cache_spot(url_Hsinchu),
            'Taichung': cache_spot(url_Taichung),
            'Kaohsiung': cache_spot(url_Kaohsiung)}


################################################ USER INPUT ##################################################
##############################################################################################################

while True:
    #date = input("What date do you want to watch a baseball game? (MM/DD)(To finish searching pleas enter 'end')")
    date = tree_reader()
    if (date == 'n') or (date == 'no'):
        print('Bye')
        sys.exit(0)
    if (date in dict_date_game) == True: 
        outcome_dict = dict_date_game[date]
        l = len(outcome_dict['time']) # how many games at that day
        break
    elif date == "end":
        sys.exit(0)
    else:
        print("No game at that date or wrong format.")


city_list = []
address_list = []
for i in outcome_dict['city']:
    address_list.append(address[city[i]])
    city_list.append(city[i])
#print(address_list)

list_top_5 = []
for add in address_list:
    places_result = cache_get_place_result(add)
    all = get_all_restaurant_with_rating__ratingNumber_address(places_result)
    top_5_restaurant = get_top_5_restaurant(all)
    list_top_5.append(top_5_restaurant)

#print(top_5_res_list) 
#print(city_list) 

printout(date)


while True:
    date = input("What other dates you want to search for? (MM/DD)(To finish searching pleas enter 'end')")
    if (date in dict_date_game) == True: 
        outcome_dict = dict_date_game[date]
        l = len(outcome_dict['time']) # how many games at that day
        printout(date)
    elif date == "end":
        sys.exit(0)
    else:
        print("No game at that date or wrong format.")

