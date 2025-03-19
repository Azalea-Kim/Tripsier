import random

from flask import Blueprint

from flask_login import current_user


from sklearn.neighbors import KNeighborsClassifier
import numpy as np

from models import *

recommened_bp = Blueprint("recommened_blue",__name__)

def recommend():
    creatVisit()
    accommodations,attractions = get_recommend_group()
    print("Acc: ",accommodations)
    print("Attr: ",attractions)
    return accommodations,attractions

def creatVisit():##更新浏览量在用户“看的时候”会更新，此处无需更新
    tagSet = set()
    tagList_accommodation = db.session.query(Accommodation.tags).distinct().all()
    tagList_attraction = db.session.query(Attraction.tags).distinct().all()
    tagSet.update(tagList_accommodation)
    tagSet.update(tagList_attraction)
    for tag in tagSet:##给每个tag创建visit
        try:
            current_visit = db.session.query(Visit).filter(Visit.user_id == current_user.id,Visit.Tag == tag[0]).one()
        except:
            current_visit = Visit(user_id = current_user.id, Tag = tag[0])
            db.session.add(current_visit)
            db.session.commit()

def knnTrain():
    # Read content of the visit and train the knn.
    feature_group = []
    score_group = []
    visit_all = db.session.query(Visit).filter(Visit.user_id == current_user.id).all()
    for visit in visit_all:
        f = []
        tags = visit.Tag.split(",")
        f.append(int(tags[0])*10) # set weight to 10
        f.append(int(tags[1]))
        f.append(int(tags[2]))
        f.append(int(tags[3]))
        feature_group.append(f)  #  Feature List
        score_group.append([visit.Visits])  #  Visit List
    knn = KNeighborsClassifier(n_neighbors = 5)
    knn.fit(feature_group, score_group)
    return knn

def knnPredict(knn,tag):
    # read the tag and update the recommend index.
    l = []
    tags = tag.split(",")
    l.append(int(tags[0])*10)
    l.append(int(tags[1]))
    l.append(int(tags[2]))
    l.append(int(tags[3]))
    l = np.array([l])
    recommened_point = int(knn.predict(l))
    return recommened_point

def get_recommend_group():
    ##读取推荐指数，加入推荐组的题号
    sums = 0
    recommend_all = db.session.query(Visit.Tag).filter(Visit.user_id == current_user.id).all()
    recommend_attraction = []
    recommend_accommodation = []
    for tag in recommend_all:##更新推荐指数
        visit = db.session.query(Visit).filter(Visit.Tag == tag[0],Visit.user_id == current_user.id).one()
        point = knnPredict(knnTrain(),visit.Tag)
        visit.Recommened_score = point
        db.session.add(visit)
        db.session.commit()

    recommend_tag = db.session.query(Visit.Tag).filter(Visit.user_id == current_user.id).order_by(desc(Visit.Recommened_score)).all()
    score_list = db.session.query(Visit.Recommened_score).filter(Visit.user_id == current_user.id).all()

    for score in score_list:
        sums = sums + score[0]

    if(sums==0):
        random.shuffle(recommend_tag)##打乱顺序，模拟随机推荐
        print("random")

    ##读取各个tag
    for tag in recommend_tag:
        accommodations = db.session.query(Accommodation).filter(tag[0] == Accommodation.tags).all()
        attractions = db.session.query(Attraction).filter(tag[0] == Attraction.tags).all()
        for attraction in attractions:
            recommend_attraction.append(attraction)

        for accommodation in accommodations:
            recommend_accommodation.append(accommodation)
    # for i in range(0,6):
    #     random_question.append(recommend_question[random.randint(26,len(recommend_question))])##随机题目
    return recommend_accommodation,recommend_attraction##高度推荐十五个，中度推荐10个，随机题目6个，分布在三个页面上




