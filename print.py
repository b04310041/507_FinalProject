list_Taipei = ['大安森林公園', '自來水園區', '蒙藏文物展示中心', '清真寺']
list_new_taipei_city = ['新莊文昌祠', '輔仁大學', '廣福宮(三山國王廟)', '新泰公園', '青年公園', '新莊武聖廟', '臺北縣立新莊體育場', '慈祐宮', '塭仔底溼地公園', '新莊中港大排親水步道']
list_Taoyuan = ['奧爾(Owl) 森林學堂', '三民公園(三民運動公園)', '虎頭山公園', '桃園親子館(原桃園三民遊客服務中心)', '第一河濱公園', '土地公文化館', '風禾公園滾輪溜滑梯']
list_Hsinchu = ['新月沙灣（坎頂與坎仔腳）', '蓮花寺', '新瓦屋客家文化園區（忠孝堂）', '溝貝親子休閒農莊', '竹北濱海遊憩區', '頭前溪豆腐岩', '問禮堂', '采田福地', '新竹縣立體育館', '拔子窟自行車道', '台灣高鐵探索館（第二代）']
list_Taichung = ['浪漫情人橋', '大坑登山步道', '大坑8號步道', '大坑9號步道', '中正露營區', '大坑5號步道', '大坑6號步道', '台中民俗公園', '崇德觀光玉市', '米笠休閒莊園(原荔園休閒農場)', '大坑4號步道', '舊社公園', '藍天白雲橋', '八二三紀念公園', '天津成衣街', '梅川公園', '大坑2號步道', '大坑1號步道', '敦化公園', '大坑3號步道']
list_Kaohsiung = ['國父紀念館（已拆除）', '大東文化藝術中心', '衛武營都會公園', '鳳儀書院', '打鐵街', '澄瀾砲台', '慈恩紀念圖書館', '平成砲台', '訓風砲台', '東便門（東福橋）', '開漳聖王廟', '曹公廟', '龍山寺', '高雄市立圖書館．曹公分館', '城隍廟', '雙慈亭']

allsite = {'Taipei':list_Taipei, 
            'new_taipei_city':list_new_taipei_city, 
            'Taoyuan':list_Taoyuan,
            'Hsinchu':list_Hsinchu,
            'Taichung':list_Taichung,
            'Kaohsiung':list_Kaohsiung}

res = [[['島瓜滷味(桃園A19環球店)', 4.8, 99, '中壢區320高鐵南路二段352號3樓'], ['藏王 日式食堂 中壢環球店', 4.8, 2055, '中壢區高鐵南路二段352號5F'], ['秋風軒鍋物 | RakutenMonkeys聯名店', 4.7, 441, '中壢區高鐵南路二段352號3樓'], ['莫平方寵物咖啡廳', 4.6, 460, '中壢區文昌路225巷32弄16號'], ['柚子花花青春客家菜(A19環球青埔店)', 4.6, 271, '中壢區高鐵南路二段352號5F']]]

from prettytable import PrettyTable

def printout(p):      
    
    x = PrettyTable()

    x.field_names = ["Date", "Time", "City", "Teams", "Site", "Restaurant","Address"]
    for i in range(l): # i = game1, game2
        

        # in case no more than 5 sites 
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
