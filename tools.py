import base64
import datetime
import random


def img_to_blob(img_dir):
    '''
    根据路径将图片转byte
    image: 必须是PIL格式
    Return Ascii encoded Pictures
    存入数据库中
    '''
    image = open(img_dir,'rb')
    b64_encoded = base64.b64encode(image.read())
    return b64_encoded.decode('ascii')

def date_calculator(start_date,end_date):
    date_s = datetime.datetime.strptime(start_date,'%Y/%m/%d')
    date_e = datetime.datetime.strptime(end_date,'%Y/%m/%d')
    res = []
    delta_days = (date_e-date_s).days
    res.append(date_s.__str__()[:10])
    for i in range(0,delta_days):
        date_s = date_s + datetime.timedelta(days = 1)
        res.append(date_s.__str__()[:10])
    return res

def plan_tester(input_content):
    text = input_content
    text_split = text.split("||")
    date_part = text_split[0]
    date_list = date_calculator(date_part.split(",")[0], date_part.split(",")[1])

    for i in range(1, len(text_split)):
        package_content = text_split[i].split(",")
        # ["acc1","attr2"]
        print(date_list[i],":",package_content[0][-1])
        for j in range(1, len(package_content)):
            print(date_list[i],":",package_content[j][-1])

def output_notion_tokens(content):
    """
    Return possible notion tokens
    for example, content could be Beijing
    return "Show me details of Beijing"
    :param content:
    :return: Token
    """
    token_list = []
    token_list.append("Please tell me the details about the "+content+".")
    token_list.append("Introduce "+content+" to me.")
    token_list.append("Could you provide more detail about "+content+"?")
    token_list.append("Tell me a story about "+content+".")
    token_list.append("Introduce a famous attraction around the "+content+".")
    token_list.append("Tell the historical story of the "+content+".")
    token_list.append("What's interesting about the "+content+".")
    token_list.append("Why do people like "+content+"?")
    return token_list[random.randint(0,len(token_list)-1)]

if __name__ == "__main__":
    print(output_notion_tokens("Beijing"))
    print(date_calculator("2023/3/15","2023/3/20"))
    plan_tester("2023/3/12,2023/3/15||acc1,attr2||acc1,attr3,attr4||acc2,attr5,attr6,attr7")