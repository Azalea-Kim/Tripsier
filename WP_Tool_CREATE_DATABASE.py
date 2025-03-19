from app import app

if __name__ == "__main__":
    from WP_Tool_InserSQL import *
    from WP_Tool_InserSQL_NEW import *
    from dispatch import init_load_table, staff_logged, staff_out, get_suitable_staff_id

    with app.app_context():
        # creat a db setting with models.
        db.drop_all()
        db.create_all()
        insert_test_destinations()
        insert_test_attractions()
        insert_test_accommodations()
        insert_user()
        insert_reviews()
        init_load_table()
        insert_reservations()
        insert_test_accommodations_ch1_ch2()
        insert_test_attractions_ch1_ch2()
        translate_database()
        pass