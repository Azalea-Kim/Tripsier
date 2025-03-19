import random
from datetime import datetime

from werkzeug.security import generate_password_hash
import random
from app import db
from models import *
from tools import img_to_blob

# 添加一些测试数据

def insert_test_destinations():
    destination1 = Destination(name="Chongqing", info="The mountain city", location="Chongqing City",
                               avatar=img_to_blob("static/temp_photo_test/city/chongqing.png"),country = "CHI",coord = "29.5330,106.5049")

    destination2 = Destination(name="Beijing", info="Beijing is the capital of the People's Republic of China.",
                               location="Beijing City",
                               avatar=img_to_blob("static/temp_photo_test/city/beijing.jpg"),country = "CHI",coord = "39.9042,116.4074")

    destination3 = Destination(name="Shanghai",
                               info="Shanghai is one of the four direct-administered municipalities of the People's Republic of China (PRC).",
                               location="Shang Hai City",
                               avatar=img_to_blob("static/temp_photo_test/city/shanghai.jpg"),country = "CHI",coord = "31.2304,121.4737")

    destination4 = Destination(name="Guangzhou",
                               info="Guang zhou  is the capital and largest city of Guangdong province in southern China.",
                               location="Guang Dong Province",
                               avatar=img_to_blob("static/temp_photo_test/city/guangzhou.jpg"),country = "CHI",coord = "23.1291,113.2644")

    destination5 = Destination(name="Hong Kong", info="The hong kong city", location="Hong Kong City",
                               avatar=img_to_blob("static/temp_photo_test/city/hongkong.png"),country = "CHI",coord = "22.2867,114.1491")

    destination6 = Destination(name="Chengdu",
                               info="Chengdu is a sub-provincial city which serves as the capital of the Chinese province of Sichuan.",
                               location="Si Chuan Province",
                               avatar=img_to_blob("static/temp_photo_test/city/chengdu.jpg"),country = "CHI",coord = "30.6595,104.0657")

    destination1.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d444252.9906780506!2d105.92539830501002!3d29.553458508621397!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x369334baf3e64f43%3A0xde9f8616dc88b321!2z5Lit5Zu96YeN5bqG5biC!5e0!3m2!1szh-CN!2sus!4v1681388390815!5m2!1szh-CN!2sus"
    destination2.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d391569.02107709314!2d116.06713495575086!3d39.938415109305666!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x35f05296e7142cb9%3A0xb9625620af0fa98a!2z5Lit5Zu95YyX5Lqs5biC!5e0!3m2!1szh-CN!2sus!4v1681388210875!5m2!1szh-CN!2sus"
    destination3.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d436718.51323912194!2d121.14643449198199!3d31.224514109018454!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x35b27040b1f53c33%3A0x295129423c364a1!2sShanghai%2C%20China!5e0!3m2!1sen!2sus!4v1683889104128!5m2!1sen!2sus"
    destination4.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d469659.2746582003!2d112.89752278737684!3d23.125885385077076!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3402f895a35c2bc7%3A0xe59e075adeae415!2sGuangzhou%2C%20Guangdong%20Province%2C%20China!5e0!3m2!1sen!2sus!4v1683889155672!5m2!1sen!2sus"
    destination5.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d236161.50322517025!2d113.81554609364626!3d22.352741963746826!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3403e2eda332980f%3A0xf08ab3badbeac97c!2sHong%20Kong!5e0!3m2!1sen!2sus!4v1683889201776!5m2!1sen!2sus"
    destination6.map_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d219655.7475493114!2d103.91039759020617!3d30.658719499247145!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x36efc52300447721%3A0xb98652ce2e240e02!2sChengdu%2C%20Sichuan%2C%20China!5e0!3m2!1sen!2sus!4v1683889227988!5m2!1sen!2sus"

    db.session.add(destination1)
    db.session.add(destination2)
    db.session.add(destination3)
    db.session.add(destination4)
    db.session.add(destination5)
    db.session.add(destination6)
    db.session.commit()

def insert_test_attractions():
    attraction1 = Attraction(name="Forbidden City",
                             avatar=img_to_blob("static/temp_photo_test/attraction/img.png"), destination_id=2,
                             info="The Palace of the Ming and Qing Dynasties, now a UNESCO World Heritage Site",
                             location="4 Jingshan Front St, Dongcheng District, Beijing, China", price="66$",score = 5,
                             tags = "2,1,3,4")

    attraction2 = Attraction(name="Temple of Heaven",
                             avatar=img_to_blob("static/temp_photo_test/attraction/img_1.png"), destination_id=2,
                             info="An ancient temple complex with stunning architecture and beautiful gardens",
                             location="1 Tiantan E Rd, Dongcheng District, Beijing, China", price="60$",score = 5,
                             tags = "2,1,5,6")


    attraction3 = Attraction(name="Summer Palace",
                             avatar=img_to_blob("static/temp_photo_test/attraction/img_2.png"), destination_id=2,
                             info="A beautiful royal garden with an ornate palace, temples, and scenic views",
                             location="19 Xinjiangongmen Rd, Haidian District, Beijing, China", price="50$"
                             ,score = 5, tags = "2,1,3,4")

    attraction4 = Attraction(name="The Great Wall of China",
                             avatar=img_to_blob("static/temp_photo_test/attraction/img_3.png"), destination_id=2,
                             info="A series of fortifications built along the northern borders of China, now a world-famous attraction",
                             location="Huairou District, Beijing, China", price="80$"
                             ,score = 5, tags = "2,1,3,5")
    attraction5 = Attraction(name="Beijing National Stadium (Bird's Nest)",
                             avatar=img_to_blob("static/temp_photo_test/attraction/img_4.png"), destination_id=2,
                             info="An iconic stadium with unique architecture that hosted the 2008 Olympics",
                             location="1 National Stadium S Rd, Chaoyang District, Beijing, China", price="70$"
                             ,score = 5, tags = "2,1,3,6")
    db.session.add(attraction1)
    db.session.add(attraction2)
    db.session.add(attraction3)
    db.session.add(attraction4)
    db.session.add(attraction5)
    db.session.commit()

def insert_test_accommodations():
    hotel1 = Accommodation(name="Luxury Hotel Beijing", info="A luxurious hotel in the heart of Beijing",
                           location="No.1 Wangfujing Street, Dongcheng District, Beijing, China", price="500$",
                           avatar=img_to_blob("static/temp_photo_test/hotel/img.png"), destination_id = 2,score = 5,
                           tags = "5,6,7,8")

    hotel2 = Accommodation(name="Beijing Palace Hotel", info="A regal hotel fit for a king",
                           location="No.9 Qianmen West Street, Dongcheng District, Beijing, China", price="700$",
                           avatar=img_to_blob("static/temp_photo_test/hotel/img_1.png"), destination_id = 2,score = 5,
                           tags = "5,4,1,2")

    hotel3 = Accommodation(name="The Grand Beijing Hotel", info="Experience luxury and sophistication in Beijing",
                           location="No.35 Chang'an Avenue, Dongcheng District, Beijing, China", price="900$",
                           avatar=img_to_blob("static/temp_photo_test/hotel/img_2.png"), destination_id = 2,score = 5,
                           tags = "5,2,3,4")

    hotel4 = Accommodation(name="Beijing Boutique Hotel", info="An intimate and stylish hotel in the heart of Beijing",
                           location="No.4 Nanluoguxiang, Dongcheng District, Beijing, China", price="600$",
                           avatar=img_to_blob("static/temp_photo_test/hotel/img_3.png"), destination_id = 2,score = 5,
                           tags = "5,3,4,6")

    hotel5 = Accommodation(name="Beijing Garden Hotel", info="Relax and rejuvenate in a lush garden setting",
                           location="No.3 Jianguomenwai Avenue, Chaoyang District, Beijing, China", price="800$",
                           avatar=img_to_blob("static/temp_photo_test/hotel/img_4.png"), destination_id = 2,score = 5,
                           tags = "5,2,7,8")


    db.session.add(hotel1)
    db.session.add(hotel2)
    db.session.add(hotel3)
    db.session.add(hotel4)
    db.session.add(hotel5)
    db.session.commit()

def insert_user():

    test_user = User(name = "Tester"
                     ,email = "2285814046@qq.com"
                     ,password = generate_password_hash("1234")
                     ,role = 0
                     ,mark = 0
                     ,avatar = img_to_blob("static/temp_photo_test/user_avatar/user_1.jpg"))

    test_user2 = User(name="Admin_Tester"
                     , email="20372103@qq.com"
                     , password=generate_password_hash("1234")
                     , role=1
                     , mark=0
                     , avatar=img_to_blob("static/temp_photo_test/user_avatar/user_1.jpg"))

    test_user3 = User(name="Admin"
                     , email="114514@qq.com"
                     , password=generate_password_hash("1234")
                     , role=1
                     , mark=0
                     , avatar=img_to_blob("static/temp_photo_test/user_avatar/user_2.jpg"))

    test_user4 = User(name="SmokerV"
                      , email="1919810@qq.com"
                      , password=generate_password_hash("1234")
                      , role=0
                      , mark=0
                      , avatar=img_to_blob("static/temp_photo_test/user_avatar/user_3.jpg"))

    db.session.add(test_user)
    db.session.add(test_user2)
    db.session.add(test_user3)
    db.session.add(test_user4)
    db.session.commit()

def insert_reviews():
    review_1 = Review_Attraction(content = "I love this attraction",
                                 rate = 4.0,
                                 sender_id = 2,
                                 attraction_id = 1
                                 )

    review_2 = Review_Attraction(content="Not very good",
                                 rate=3.0,
                                 sender_id=3,
                                 attraction_id=1
                                 )
    db.session.add(review_1)
    db.session.add(review_2)
    db.session.commit()

def insert_reservations():
    for i in range(0,80):
        month = random.randint(1,12)
        day = random.randint(1,30)
        if(month==2):
            day = random.randint(1,28)
        date = "2023/" + str(month) + "/" +str(day)
        date = datetime.strptime(date, '%Y/%m/%d')
        r1 = Reservation_Accommodation(user_id = random.randint(1,4),accommodation_id = random.randint(1,5),date = date,note = "Hi Manager")
        r2 = Reservation_Attraction(user_id = random.randint(1,4),attraction_id = random.randint(1,5),date = date,note = "Hi Manager")
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

# def insert_carts():
#     for i in range(0,80):
#         month = random.randint(1,12)
#         day = random.randint(1,30)
#         if(month==2):
#             day = random.randint(1,28)
#         date = "2023/" + str(month) + "/" +str(day)
#         date = datetime.strptime(date, '%Y/%m/%d')
#         r1 = Reservation_Accommodation(user_id = random.randint(1,4),accommodation_id = random.randint(1,5),date = date,note = "Hi Manager")
#         r2 = Reservation_Attraction(user_id = random.randint(1,4),attraction_id = random.randint(1,5),date = date,note = "Hi Manager")
#         db.session.add(r1)
#         db.session.add(r2)
#         db.session.commit()

def insert_tags():
    tag1 = Tag(id = 1, content = "Natural scenery")
    tag2 = Tag(id = 2, content = "Historical and cultural")
    tag3 = Tag(id = 3, content = "Theme park")
    tag4 = Tag(id = 4, content = "Culinary experience")
    tag5 = Tag(id = 5, content = "Luxury")
    tag6 = Tag(id = 6, content = "Landmarks and monuments")
    tag7 = Tag(id = 7, content = "Nighttime sightseeing")
    tag8 = Tag(id = 8, content = "Sports and leisure")
    tag9 = Tag(id = 9, content = "Adventure and exploration")

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)
    db.session.add(tag5)
    db.session.add(tag6)
    db.session.add(tag7)
    db.session.add(tag8)
    db.session.add(tag9)
    db.session.commit()