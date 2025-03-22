from PIL import ImageFont, ImageDraw, Image
from datetime import datetime, timedelta
import json, random, requests, configparser as cp, re

config = cp.ConfigParser()
config.read('config.ini')

class NoMealError(Exception):
    def __init__(self):
        super().__init__("급식 정보가 없습니다. meal.json 파일을 확인하거나 올바른 날짜 설정인지 확인해주세요.")

def get_meal_data(day):

    # ------------------------------------------------------------------- 특수 날짜
    if day == "20241206": return "딸기샌드위치\n우유생크림빵\n초콜릿드링크"
    if day == "20241211": return "대만샌드위치\n딸기맛도넛\n달걀\n오렌지쥬스"
    # ------------------------------------------------------------------- 특수 날짜

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&KEY={config['nice']['key']}&ATPT_OFCDC_SC_CODE={config['nice']['region']}&SD_SCHUL_CODE={config['nice']['school']}&MLSV_YMD={day}"
    headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
    req = requests.get(url, headers=headers)
    meal_data = []
    json_data = json.loads(req.text)
    try:
        meal_data2 = json_data["mealServiceDietInfo"][1]["row"]
    except: raise NoMealError
    else:
        for i in meal_data2:
            # m = str(i['DDISH_NM']).replace('<br/>', '\n').replace('  ', ' ').replace('(고)', '')
            # m = str(i['DDISH_NM']).replace('<br/>', '\n').split('(')[0]
            m = str(i['DDISH_NM']).split('<br/>')
            a = []
            for j in m:
                j = j.split('(')[0].strip()
                a.append(j)
            # pattern = re.compile('[ㄱ-ㅎ가-힣]+')
            # matches = pattern.findall(m)

            # m = '\n'.join(matches)
            m = '\n'.join(a)
            meal_data.append(m)
            # meal_data.append(f"{i['MMEAL_SC_NM']}\n\n{m}")
        meal_data = "\n".join(meal_data)
    return meal_data

def make_meal_week():
    def getsize(font, text):
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top

    # with open("meal.json", "r", encoding="UTF-8") as f:
    #     meal = json.load(f)

    result = []

    for i in range(1, 6):
        img = Image.open("week_meal_back.png")

        f_s = 75
        font = ImageFont.truetype("KHNPHDotfR.otf", f_s, encoding="UTF-8")

        f_s2 = 50
        font2 = ImageFont.truetype("KHNPHDotfR.otf", f_s2, encoding="UTF-8")
        # w, h = img.size
        # text = "치킨마요덮밥 \n콩나물국 \n떡꼬치 \n참나물겉절이 \n깍두기 \n레몬에이드"
        text = ""
        # date = (datetime.now() + timedelta(days=12)).strftime("%m월 %d일")
        date = (datetime.now() + timedelta(days=i)).strftime("%m월 %d일")
        # date = (datetime.now() + timedelta(days=3-i)).strftime("%m월 %d일")
        try: text = get_meal_data((datetime.now() + timedelta(days=i)).strftime("%Y%m%d"))
        # try: text = get_meal_data((datetime.now() + timedelta(days=2+i)).strftime("%Y%m%d"))
        # except: text = "급식 정보가 없습니다."
        except: continue
        # print(text)
        meals = text

        tw, th = getsize(font, text)
        draw = ImageDraw.Draw(img)
        # (int(w/2)-tw/2, int(h/2)-int(font.size/2))
        # 384654
        # draw.text((512, 420), text, font=font, fill="#97BECF", align="center", anchor="ms")
        
        h = 400
        text = str(text).split("\n")
        for i in text:
            draw.text((512, h), i, font=font, fill="black", align="center", anchor="ms")
            h += 75
        # draw.text((512, 420), text, font=font, fill="black", align="center", anchor="ms")
        draw.text((638, 50), date, font=font2, fill="#9E9E9E")
        ra = random.randint(10000, 99999)
        name = f"{date.replace(' ', '').replace('월', '').replace('일', '')}{ra}"
        img.save(f"C:/xampp/htdocs/images/week_meals/{name}.png")
        img.save(f"C:/Users/Administrator/Desktop/meal_system/week_meals/{name}.png")
        result.append([date, name, meals])
    
    img = Image.open("week_meal.png")

    f_s = 75
    font = ImageFont.truetype("KHNPHDotfR.otf", f_s, encoding="UTF-8")

    f_s2 = 50
    font2 = ImageFont.truetype("KHNPHDotfR.otf", f_s2, encoding="UTF-8")
    # w, h = img.size
    # text = "치킨마요덮밥 \n콩나물국 \n떡꼬치 \n참나물겉절이 \n깍두기 \n레몬에이드"
    text = ""
    # date = (datetime.now() + timedelta(days=12)).strftime("%m월 %d일")
    date = (datetime.now() + timedelta(days=1)).strftime("%m월 %d일")
    date2 = (datetime.now() + timedelta(days=5)).strftime("%m월 %d일")

    tw, th = getsize(font, text)
    draw = ImageDraw.Draw(img)
    # (int(w/2)-tw/2, int(h/2)-int(font.size/2))
    # 384654
    # draw.text((512, 420), text, font=font, fill="#97BECF", align="center", anchor="ms")

    # draw.text((512, 420), text, font=font, fill="black", align="center", anchor="ms")
    draw.text((512, 662), f"({date} ~ {date2})", font=font2, fill="#9E9E9E", align="center", anchor="ms")
    ra = random.randint(10000, 99999)
    name = f"back_{date.replace(' ', '').replace('월', '').replace('일', '')}{ra}"
    img.save(f"C:/xampp/htdocs/images/week_meals/{name}.png")
    img.save(f"C:/Users/Administrator/Desktop/meal_system/week_meals/{name}.png")
    
    return [name, f'({date} ~ {date2})'], result