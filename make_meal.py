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
    # if day == "20241017": return "1차 지필평가(1)\n\n한 줄기 햇살이\n어둠을 가르듯\n당신의 노력이\n결실을 맺기를"
    # if day == "20241018": return "1차 지필평가(2)\n\n어려움 끝에는\n행복이 있다\n당신의 노력이\n찬란히 빛나기를"
    # if day == "20241021": return "1차 지필평가(3)\n\n열심히 노력하고\n준비한 만큼\n후회 없이\n발휘하기를"
    # if day == "20241022": return "1차 지필평가(4)\n\n결과에 대한 걱정은\n잠시 접어두고\n자신감을 갖고\n마지막까지 힘내기를"

    if day == "20241206": return "딸기샌드위치\n우유생크림빵\n초콜릿드링크"
    if day == "20241211": return "대만샌드위치\n딸기맛도넛\n달걀\n오렌지쥬스"
    if day == "20241225": return "Merry Christmas!\n\n크리스마스\n행복한 시간\n보내세요!"

    if day == "20241216": return "2차 지필평가(1)\n\n오늘의 시험은\n내일의 더 큰\n성공을 위한\n시작"
    if day == "20241217": return "2차 지필평가(2)\n\n할 수 있는\n최선을 다하는 것\n그것만으로\n충분"
    if day == "20241218": return "2차 지필평가(3)\n\n차곡차곡 쌓은\n하루하루가\n빛나는 결과로\n보답받기를"
    if day == "20241219": return "2차 지필평가(4)\n\n펜이 가는\n길마다\n정답이\n되기를"
    if day == "20241220": return "2차 지필평가(5)\n\n지금까지\n잘 해왔으니\n마지막까지\n힘내기를"

    if day == "20250225": return "급식 자동 생성\n\n테스트"
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

def make_meal():
    def getsize(font, text):
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top

    # with open("meal.json", "r", encoding="UTF-8") as f:
    #     meal = json.load(f)

    

    img = Image.open("background.png")

    f_s = 75
    font = ImageFont.truetype("KHNPHDotfR.otf", f_s, encoding="UTF-8")

    f_s2 = 50
    font2 = ImageFont.truetype("KHNPHDotfR.otf", f_s2, encoding="UTF-8")

    # w, h = img.size
    # text = "치킨마요덮밥 \n콩나물국 \n떡꼬치 \n참나물겉절이 \n깍두기 \n레몬에이드"
    text = ""
    # date = (datetime.now() + timedelta(days=12)).strftime("%m월 %d일")
    date = (datetime.now()).strftime("%m월 %d일")
    # try: text = meal[date]
    # try: text = get_meal_data((datetime.now() + timedelta(days=6)).strftime("%Y%m%d"))
    try: text = get_meal_data(datetime.now().strftime("%Y%m%d"))
    # except: text = "급식 정보가 없습니다."
    except: raise(NoMealError)

    # meals = meal[date]
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
    draw.text((708, 50), date, font=font2, fill="#9E9E9E")
    ra = random.randint(10000, 99999)
    name = f"{date.replace(' ', '').replace('월', '').replace('일', '')}{ra}"
    img.save(f"C:/xampp/htdocs/images/meal/{name}.png")
    img.save(f"C:/Users/Administrator/Desktop/meal_system/meals/{name}.png")

    img2 = Image.open(f"background22.png")
    img3 = Image.open(f"C:/Users/Administrator/Desktop/meal_system/meals/{name}.png")
    img2.paste(img3, box=(0, 512))
    # img2.save("test.png")
    img2.save(f"C:/xampp/htdocs/images/meal/8888{name}.png")
    img2.save(f"C:/Users/Administrator/Desktop/meal_system/meals/8888{name}.png")
    return date, name, meals