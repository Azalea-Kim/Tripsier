import random
from time import sleep

from werkzeug.security import generate_password_hash
import random

from Baidu_trans import Translator
from app import db
from models import *

from tools import img_to_blob


# 添加一些测试数据


def insert_test_attractions_ch1_ch2():
    root_pace = "static/temp_photo_test/attraction/"
    # Attractions of chongqing
    Three_Gorges_Museum = Attraction(name="Three Gorges Museum", avatar=img_to_blob(root_pace + "aaa.jpg"),
                                     destination_id=1,
                                     info="The collection is mainly the preservation and related explanations before "
                                          "and after the construction of the Three Gorges Dam",
                                     location="No.236 Renmin Road, Chongqing", price="66$", score=5, tags="4,2,7,8")
    Chongqing_Peoples_Square = Attraction(name="Chongqing_People's_Square",
                                          avatar=img_to_blob(root_pace + "001.jpg"), destination_id=1,
                                          info="This People's Square and the Three Gorges Museum are next to each "
                                               "other, which is very lively",
                                          location="In front of the Great Hall of the People, No. 173 Renmin Road, "
                                                   "Chongqing", price="32$", score=5, tags="4,2,3,5")
    Katsura_Garden = Attraction(name="Katsura_Garden",
                                avatar=img_to_blob(root_pace + "002.jpg"), destination_id=1,
                                info="This is the mansion of Mr. Zhang Zhizhong, a former Kuomintang general, "
                                     "named \"Guiyuan\" because of the two osmanthus trees planted in the courtyard",
                                location="No. 65, Zhongshan 4th Road, Yuzhong District", price="12$", score=5,
                                tags="4,2,3,6")
    # Attractions of shanghai
    The_Bund_of_the_Huangpu_River = Attraction(name="The Bund of the Huangpu River",
                                               avatar=img_to_blob(root_pace + "003.png"), destination_id=3,
                                               info="Walking along the Bund is one of the must-do things for visitors "
                                                    "to Shanghai the Bund is one of Shanghai's most famous tourist "
                                                    "attractions",
                                               location=" Located on the west side of the Huangpu River", price="15$",
                                               score=5, tags="4,5,2,3")
    Oriental_Pearl_Tower = Attraction(name="Oriental Pearl Tower",
                                      avatar=img_to_blob(root_pace + "004.png"), destination_id=3,
                                      info="The Oriental Pearl Tower is the tallest tower in Asia and one of "
                                           "Shanghai's landmark buildings",
                                      location=" Shanghai Huangpu River", price="33$", score=5, tags="3,2,4,7")
    Shanghai_Disneyland = Attraction(name="Shanghai Disneyland", avatar=img_to_blob(root_pace + "005.jpg"),
                                     destination_id=3,
                                     info="Shanghai Disneyland is the first Disney theme park in Chinese mainland and "
                                          "is a must-see attraction for young people visiting Shanghai",
                                     location="Chuansha New Town, Pudong New Area, Shanghai, China", price="33$",
                                     score=5, tags="3,2,4,7")
    # Attractions of guangzhou
    Million_sunflower_garden = Attraction(name="Million sunflower garden", avatar=img_to_blob(root_pace + "006.png"),
                                          destination_id=4,
                                          info="Million Sunflower Garden is the first park in China to use sunflowers "
                                               "as ornamental plants and design them as a large-scale themed garden.",
                                          location="Guangzhou City, Guangdong Province, Nansha District, Wanqingsha "
                                                   "Town, Xinken 15",
                                          price="20$", score=5, tags="3,3,6,3")
    Basilica_of_the_Sacred_Heart_of_the_Stone_Chamber = Attraction(
        name="Basilica of the Sacred Heart of the Stone Chamber", avatar=img_to_blob(root_pace + "007.png"),
        destination_id=4,
        info="The Basilica of the Sacred Heart is the largest church in the Catholic Diocese of Guangzhou and one of "
             "the four all-stone Gothic church buildings in the world.",
        location="No. 56-7, former Yide Road, Yuexiu District, Guangzhou, Guangdong Province", price="13$", score=5,
        tags="3,2,5,7")

    Baiyun_Mountain = Attraction(name="Baiyun Mountain", avatar=img_to_blob(root_pace + "008.png"), destination_id=4,
                                 info="The mountains and forests after the rain are even more beautiful, and the "
                                      "clouds and mist on the mountains seem to be in a fairyland.",
                                 location=" No. 801, Guangyuan Middle Road, Baiyun District, Guangzhou", price="50$",
                                 score=5, tags="3,2,5,7")

    # HongKong
    ha1 = Attraction(name="Ocean Park Hong Kong", avatar=img_to_blob(root_pace + "009.png"), destination_id=5,
                     info="The world's largest aquarium, shark house and ocean theater show dolphins, "
                          "sea lions, killer whales and other wonderful stunts, roller coaster, "
                          "Ferris wheel, pirate ship and so on. All kinds of motorized rides.",
                     location=" No. 801, HongKong Middle Road, Baiyun District, HongKong", price="50$",
                     score=5, tags="3,2,4,7")
    ha2 = Attraction(name="Repulse bay", avatar=img_to_blob(root_pace + "010.png"), destination_id=5,
                     info="South of Victoria Peak on Hong Kong Island, the bay is in the shape of a "
                          "crescent, known as the \"first bay under heaven\", also known as the "
                          "\"Oriental Hawaii\".",
                     location=" No.77, HongKong Center Road, Baiyun District, HongKong", price="50$",
                     score=5, tags="3,2,4,7")
    ha3 = Attraction(name="Victoria Harbour", avatar=img_to_blob(root_pace + "011.png"), destination_id=5,
                     info="One of the world's three great ports, also has: \"Pearl of the Orient\" and "
                          "\"three world night scenery\" reputation.",
                     location=" No.103, ChaoYang Middle Road, Baiyun District, HongKong", price="50$",
                     score=5, tags="3,5,6,7")

    ca1 = Attraction(name="Jiuzhaigou Valley", avatar=img_to_blob(root_pace + "012.png"), destination_id=6,
                     info="The extraordinary natural scenery and strong ethnic customs complement each other. There are nine Tibetan villages in Jiuzhaigou, including many scenic spots.",
                     location=" No.103, ChaoYang Middle Road, Baiyun District, Chengdu", price="50$",
                     score=5, tags="4,2,8,7")
    ca2 = Attraction(name="Huanglong scenic spot", avatar=img_to_blob(root_pace + "013.png"), destination_id=6,
                     info="It is listed as a World Natural Heritage site by UNESCO",
                     location=" No.103, ChaoYang Middle Road, Baiyun District, Chengdu", price="50$",
                     score=5, tags="3,5,4,7")
    ca3 = Attraction(name="Emei Mountain", avatar=img_to_blob(root_pace + "014.png"), destination_id=6,
                     info="The sunrise of Mount Emei and the surging sea of clouds are enough to count.",
                     location=" No.103, ChaoYang Middle Road, Baiyun District, Chengdu", price="50$",
                     score=5, tags="3,5,8,6")

    attractions = [Three_Gorges_Museum, Chongqing_Peoples_Square, Katsura_Garden, The_Bund_of_the_Huangpu_River,
                   Oriental_Pearl_Tower, Shanghai_Disneyland, Million_sunflower_garden,
                   Basilica_of_the_Sacred_Heart_of_the_Stone_Chamber, Baiyun_Mountain, ha1, ha2, ha3, ca1, ca2, ca3]
    db.session.add_all(attractions)
    db.session.commit()


def insert_test_accommodations_ch1_ch2():
    root_pace = "static/temp_photo_test/hotel/"
    ch1 = Accommodation(name="Chongqing Jiefangbei Westin Hotel",
                        info="Every room in the hotel offers air conditioning, iPod dock, satellite TV and electric "
                             "kettle. Private bathroom with shower, tub and hair dryer.",
                        location="No.222 Xinhua Road, Yuzhong District, Chongqing, China", price="1000¥",
                        avatar=img_to_blob(root_pace + "ch1.png"), destination_id=1, score=5, tags="5,2,4,3")

    ch2 = Accommodation(name="Doubletree by Hilton Chongqing Jiangbei",
                        info="Elegant rooms with ironing facilities, mini bar and tea/coffee making facilities.",
                        location="Building B, Xiexin Center, No.68 Yanghe 1st Road, Jiangbei District, Chongqing",
                        price="540¥",
                        avatar=img_to_blob(root_pace + "ch2.png"), destination_id=1, score=5, tags="5,3,4,8")

    ch3 = Accommodation(name="Chongqing International Trade Glenview Hotel",
                        info="The metro station is a five-minute walk away and offers an indoor swimming pool and "
                             "fitness center.",
                        location="No.11 Jianguomenwai Avenue, Chaoyang District, Chongqing, China", price="581.74¥",
                        avatar=img_to_blob(root_pace + "ch3.png"), destination_id=1, score=5, tags="5,4,3,2")

    ch4 = Accommodation(name="Chongqing Marriott Hotel",
                        info="2.3 kilometers away from the People's Liberation Monument, there is a Spa center",
                        location="No.65 Xinhua Road, Nanan District, Chongqing, China", price="650¥",
                        avatar=img_to_blob(root_pace + "ch4.png"), destination_id=1, score=5, tags="5,3,4,6")

    ch5 = Accommodation(name="Raffles Intercontinental Chongqing",
                        info="Equipped with fitness center, free private parking",
                        location="No.65 Xishan Road, Yuzhong District, Chongqing, China", price="1400¥",
                        avatar=img_to_blob(root_pace + "ch5.png"), destination_id=1, score=5, tags="5,6,4,8")

    # Hotels of Beijing
    # TODO: Adds attractions for the other destinations

    sh1 = Accommodation(name="Shanghai Jianguo Hotel",
                        info="The hotel has more than 200 rooms, all equipped with 55 inch LCD TV",
                        location="No.65 Chuansha Road, Pudong New Area, Shanghai, China", price="508¥",
                        avatar=img_to_blob(root_pace + "sh1.png"), destination_id=3, score=5, tags="6,4,3,7")
    sh2 = Accommodation(name="Pu Yan Hotel on the Bund",
                        info="Close to the No. 2 and No. 10 subway lines, convenient access",
                        location="No.65 Xishan Road, Di Suzhou River, East Beijing Road, Shanghai, China",
                        price="1006¥",
                        avatar=img_to_blob(root_pace + "sh2.png"), destination_id=3, score=5, tags="6,4,2,8")
    sh3 = Accommodation(name="Huayuan Hall on the Bund - Joy Garden",
                        info="There are tall and steep Art Deco style steepled churches, bustling old commercial "
                             "streets",
                        location="No.65 The hinterland of Cheng-Huang Yu Garden, Shanghai, China", price="1400¥",
                        avatar=img_to_blob(root_pace + "sh3.png"), destination_id=3, score=5, tags="6,3,4,2")

    gh1 = Accommodation(name="Guangzhou design capital County elegant hotel",
                        info="Over 1000 square meters of banquet and conference facilities, four distinctive "
                             "restaurants",
                        location="No.150 Huangbian North Road, Baiyun District, Guangzhou, Guangdong, China",
                        price="300¥",
                        avatar=img_to_blob(root_pace + "gh1.png"), destination_id=4, score=5, tags="6,5,3,2")
    gh2 = Accommodation(name="Victoria Hotel",
                        info="It's about a five-minute walk to the subway station with restaurants downstairs.",
                        location="Lobby, 1st Floor, East Tower, Aoyuanyue Times Square, 283 Hanxi Avenue West, "
                                 "Panyu District, Guangzhou, Guangdong, China",
                        price="390",
                        avatar=img_to_blob(root_pace + "gh2.png"), destination_id=4, score=5, tags="6,4,3,2")
    gh3 = Accommodation(name="Knorami International Apartments",
                        info="Free breakfast and 24 hours free shuttle service from airport and subway station",
                        location="Room 1203, Apartment C, Huijin International Financial Center, 660 Huangpu Avenue "
                                 "Middle, Tianhe District, Guangzhou, Guangdong, China",
                        price="1400¥",
                        avatar=img_to_blob(root_pace + "gh3.png"), destination_id=4, score=5, tags="6,2,4,7")
    gh4 = Accommodation(name="Kapok cyanine",
                        info="Free breakfast and 24 hours free shuttle service from airport and subway station",
                        location="No.18, Second Lane of Aigang Longxizhuang, Renhe Town, Baiyun District, Guangzhou, "
                                 "Guangdong, China",
                        price="1400¥",
                        avatar=img_to_blob(root_pace + "gh4.png"), destination_id=4, score=5, tags="6,5,4,2")

    hh1 = Accommodation(name="The Langham Hotel in Hong Kong",
                        info="Intimate personal services include 24-hour room service, laptop workspace and other "
                             "comforts",
                        location="8 Beijing Road, Tsim Sha Tsui, Yau Tsim Mong District, Hong Kong, China",
                        price="2310¥",
                        avatar=img_to_blob(root_pace + "hh1.png"), destination_id=5, score=5, tags="6,3,4,5")
    hh2 = Accommodation(name="Hong Kong Island Shangri-la",
                        info="The location is excellent. Bustling city scene, spectacular Victoria Harbour, popular "
                             "cultural attractions and high-end shopping malls are within easy reach",
                        location="Pacific Place, Central Court Road, Admiralty, Central Western, Hong Kong, China",
                        price="4680¥",
                        avatar=img_to_blob(root_pace + "hh2.png"), destination_id=5, score=5, tags="6,2,4,7")

    cdh1 = Accommodation(name="Chengdu Ruicheng Celebrity Hotel",
                         info="Each guest room is equipped with small dolls and red panda mouthwash cups to warm the "
                              "family for a whole trip.",
                         location="No.68 Renmin Middle Road, Section 2, Qingyang District, Chengdu, Sichuan, China",
                         price="400¥",
                         avatar=img_to_blob(root_pace + "cdh1.png"), destination_id=6, score=5, tags="6,3,5,7")
    cdh2 = Accommodation(name="Chengdu Xinliang Hotel",
                         info="Free breakfast and 24 hours free shuttle service from airport and subway station",
                         location="No.246 Dongdajie Section, Dongdajie, Jinjiang District, Chengdu, Sichuan, China",
                         price="1400¥",
                         avatar=img_to_blob(root_pace + "cdh2.png"), destination_id=6, score=5, tags="6,2,4,7")
    cdh3 = Accommodation(name="Chengdu City Celebrity Hotel",
                         info="Free breakfast and 24 hours free shuttle service from airport and subway station",
                         location="122-124 Renmin South Road, Qingyang District, Chengdu, Sichuan, China",
                         price="870¥",
                         avatar=img_to_blob(root_pace + "cdh3.png"), destination_id=6, score=5, tags="6,5,4,3")
    cdh4 = Accommodation(name="Hyatt Hotel Langpo Chengdu",
                         info="The airport apron on the 63rd floor overlooks the city and the snowy mountains, making it a unique choice for outdoor activities in downtown Chengdu",
                         location="Building 2, West International Financial Center, 258 East Street Section, Jinjiang District, Chengdu, Sichuan, China",
                         price="1400¥",
                         avatar=img_to_blob(root_pace + "cdh4.png"), destination_id=6, score=5, tags="6,4,2,3")

    hotels = [ch1, ch2, ch3, ch4, ch5, sh1, sh2, sh3, gh1, gh2, gh3, gh4, hh1, hh2, cdh1, cdh2,
              cdh3, cdh4]
    db.session.add_all(hotels)
    db.session.commit()


def translate_database():
    destinations = Destination.query.all()

    accommodations = Accommodation.query.all()
    d_q = ""
    for destination in destinations:
        d_q = d_q + destination.name + "\n" + destination.info + "\n" + destination.location + "\n"
    resp = Translator.translate(d_q)
    for destination in destinations:
        destination.name_cn = resp.pop(0)["dst"]
        destination.info_cn = resp.pop(0)["dst"]
        destination.location_cn = resp.pop(0)["dst"]
        db.session.add(destination)
    db.session.commit()
    sleep(1)

    trans_attractions()
    trans_accommodation()


def trans_attractions():
    divide_trans_a(1, 4)
    sleep(1)
    divide_trans_a(5, 8)
    sleep(1)
    divide_trans_a(9, 12)
    sleep(1)
    divide_trans_a(13, 16)
    sleep(1)
    divide_trans_a(17, 19)
    sleep(1)

def trans_accommodation():
    divide_trans_ac(1, 4)
    sleep(1)
    divide_trans_ac(5, 8)
    sleep(1)
    divide_trans_ac(9, 12)
    sleep(1)
    divide_trans_ac(13, 16)
    sleep(1)
    divide_trans_ac(17, 20)
    sleep(1)
    divide_trans_ac(21, 23)
    sleep(1)




def divide_trans_a(i, n):
    i -= 1
    a_q = ""
    attractions = Attraction.query.all()
    a1 = []
    while i < n:
        print(i)
        a_q = a_q + attractions[i].name + "\n" + attractions[i].info + "\n" + attractions[i].location + "\n"
        a1.append(attractions[i])
        i += 1
    resp = Translator.translate(a_q)
    for attraction in a1:
        attraction.name_cn = resp.pop(0)["dst"]
        attraction.info_cn = resp.pop(0)["dst"]
        attraction.location_cn = resp.pop(0)["dst"]
        db.session.add(attraction)
    db.session.commit()


def divide_trans_ac(i, n):
    i -= 1
    a_q = ""
    accommodations = Accommodation.query.all()
    a1 = []
    while i < n:
        print(i)
        a_q = a_q + accommodations[i].name + "\n" + accommodations[i].info + "\n" + accommodations[i].location + "\n"
        a1.append(accommodations[i])
        i += 1
    resp = Translator.translate(a_q)
    for attraction in a1:
        attraction.name_cn = resp.pop(0)["dst"]
        attraction.info_cn = resp.pop(0)["dst"]
        attraction.location_cn = resp.pop(0)["dst"]
        db.session.add(attraction)
    db.session.commit()
