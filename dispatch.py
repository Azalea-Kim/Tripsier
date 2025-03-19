from main import db
from models import User

"""
    调度算法 员工负载记录表
    :key staff_id
    :value 目前的负载,下线员工负载为 inf_num (99999999)
    按照负载数动态返回staff的id
"""
staff_dict = {}
inf_num = 99999999

def init_load_table():
    """
    Load the staff's id to the table and init them
    :return: None
    """
    staff_id_list = db.session.query(User.id).filter(User.role == 1).all()
    for id in staff_id_list:
        staff_dict[id] = inf_num

def staff_logged(id):
    """
    Update when a staff logged in this system
    :param id: staff id
    :return: None
    """
    staff_dict[id] = 0

def staff_out(id):
    """
    Update when a staff logout from this system
    :param id: staff id
    :return: None
    """
    staff_dict[id] = inf_num

def start_communication(id):
    """
       Update when a staff communicate with a customer
       :param id: staff id
       :return: None
    """
    staff_dict[id] = staff_dict[id] + 1

def communication_end(id):
    """
       Update when a staff communicate with a customer
       :param id: staff id
       :return: None
    """
    staff_dict[id] = staff_dict[id] - 1

def get_suitable_staff_id():
    """
    get the best staff id for the customer
    :return: the staff id
    """
    min_value = inf_num
    for id,value in staff_dict.items():
        if(min_value>value):
            min_value = value
    if(min_value == inf_num):
        # No available Staff now
        return "No"
    else:
        return min_value


