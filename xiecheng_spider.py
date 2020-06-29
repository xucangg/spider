import time
import random
import math
import re

from selenium.webdriver import Ie
from selenium.webdriver.common.keys import Keys

hotels = [
    ['6929152', "景莱酒店(上海外滩店)"],
    ['18431318', "全季酒店(上海外滩金陵东路店)"],
    ['756484', "锦江都城经典酒店(上海南京路步行街南京饭店)"],
    ['419388', "全季酒店(上海外滩宁波路店)"],
    ['23852115', "宿适轻奢酒店(上海人名广场地铁站店)"],
    ['8052290', "全季酒店(上海外滩九江路店)"],
    ['3919405', "桔子酒店·精选(上海外滩外白渡桥店)"],
    ['6476016', "汉庭酒店(上海外滩延安东路店)"],
    ['1480662', "全季酒店(上海外滩山东中路店)"]
]
hotel_info_text = open('酒店房间价格.txt', 'w', encoding='utf-8')

ie = Ie(executable_path='C:\\Users\\kenny\\Desktop\\IEDriverServer.exe')
ie.get('https://hotels.ctrip.com')
#button = ie.find_element_by_xpath("//div[@id='J_SwitchSearch']/div[@class='search_btn2']/input")


def spider(hotel):
    time.sleep(math.ceil(random.random()*3))
    search_input = ie.find_element_by_id("txtKeyword")
    search_input.send_keys("{}".format(hotel[1]))
    time.sleep(math.ceil(random.random()*3))
    ie.find_element_by_id("btnSearch").send_keys(Keys.ENTER)
    time.sleep(math.ceil(random.random()*10))
    url = ie.find_element_by_xpath("//div[@id={}]/ul/li[@class='hotel_item_name']/h2/a".format(hotel[0]))
    ie.execute_script("arguments[0].scrollIntoView();", url)
    time.sleep(5)
    url.send_keys(Keys.ENTER)
    time.sleep(10)
    windows = ie.current_window_handle
    all_handles = ie.window_handles
    for handle in all_handles:
        if handle != windows:
            ie.switch_to.window(handle)
    time.sleep(30)
    rooms = ie.find_element_by_xpath("//div[@id='hotelRoomBox']")
    room_nums = re.split('查看详情', rooms.text)
    room_type = []
    room_info= {}
    room_type_code = []

    for i in list(range(1, len(room_nums)-1)):
        room_type.append(room_nums[i].split('\n')[-2])

    for i in list(range(2,len(room_nums))):
        room_type_code.append(room_nums[i].split('预订'))

    for i in list(range(len(room_type_code))):
        info = []
        for j in list(range(0, len(room_type_code[i])-1)):
            code = re.search('编号:\w+', room_type_code[i][j]).group()
            try:
                types = re.search('标准价', room_type_code[i][j]).group()
            except AttributeError:
                types = '钟点房(08:00~22:00)'
            price = re.search('\u00A5\d+', room_type_code[i][j]).group()
            info.append((code, types, price))
        room_info[room_type[i]] = info
    

    hotel_info_text.write('-'*32+hotel[1]+'-'*32+'\n')
    for i in room_info:
        hotel_info_text.write(i+':'+'\n')
        for j in room_info[i]:
            code = j[0]
            types = j[1]
            price = j[2]
            hotel_info_text.write(' '*4+code+' '+ types+' '+ price+'\n')

    ie.close()
    ie.switch_to.window(windows)
    ie.find_element_by_id("txtKeyword").send_keys(Keys.CONTROL+'a')
    ie.find_element_by_id("txtKeyword").send_keys(Keys.DELETE)

for i in hotels:
    spider(i)
    time.sleep(5)
hotel_info_text.close()
ie.close()
