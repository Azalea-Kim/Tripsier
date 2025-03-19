@wp_3.route("/tabs", methods=["POST", "GET"])
def tabs():
    "2023/3/12,2023/3/15||acc1,attr2||acc1,attr3,attr4||acc2,attr5,attr6,attr7"
    text = request.form.get("text")
    text = text.replace("-", "/")
    print("Text: ", text)
    '2023/05/13,2023/05/14||attr3,||attr7,||'
    g.append(text)
    text_split = text.split("||")
    date_part = text_split[0]
    date_list = date_calculator(date_part.split(",")[0], date_part.split(",")[1])
    g.append(date_list)

    #
    # pln = Planning(user_id=current_user.id, encoded_content=date_list)
    # db.session.add(pln)
    # db.session.commit()

    dates = []
    # nowTime = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S")

    nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
    print(type(nowTime))
    print(nowTime)
    g.append("now")
    print(date_list)
    for i in range(1, len(text_split)-1):
        g.append("hi")
        package_content = text_split[i].split(",")
        if ("" in package_content):
            package_content.remove("")
        # ["acc1","attr2"]
        print("i")
        print(i)
        date = datetime.strptime(date_list[i - 1], '%Y-%m-%d')
        dates.append(date)
        order = 0
        for obj in package_content:
            g.append("in")
            if ("attr" in obj):
                attraction_reservation = Reservation_Attraction(user_id=current_user.id, date=date,
                                                                attraction_id=int(obj[-1]), order=order,
                                                                book_date=nowTime)
                db.session.add(attraction_reservation)
                db.session.commit()

                res = Reservations(user_id=current_user.id, date=date,
                                   a_id=int(obj[-1]), order=order,
                                   book_date=nowTime, type=1)
                db.session.add(res)
                db.session.commit()

                order += 1
            elif ("acc" in obj):
                acc_reservation = Reservation_