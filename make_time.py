from PIL import ImageFont, ImageDraw, Image
from emoji import unicode_codes

from datetime import datetime, timedelta
import json, random, requests, configparser as cp, re

config = cp.ConfigParser()
config.read('config.ini')

class NoTimeError(Exception):
    def __init__(self):
        super().__init__("급식 순번 정보가 없습니다. meal_time.json을 확인해주세요.")

def get_time(day):
    with open("meal_time.json", "r", encoding="UTF-8") as f:
        meal = json.load(f)
    try: meal = meal[day]
    except: raise(NoTimeError)
    size = [f"{i}반" for i in range(1, 13)]
    if meal == 12 or meal == 9 or meal == 6 or meal == 3: size.reverse()
    result = []
    if meal == 12:
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 9:
        size = size[3:] + size[:3]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 6:
        size = size[6:] + size[:6]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 3:
        size = size[9:] + size[:9]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")

    if meal == 1:
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 4:
        size = size[3:] + size[:3]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 7:
        size = size[6:] + size[:6]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    if meal == 10:
        size = size[9:] + size[:9]
        for i in range(0, 12):
            if i % 3 == 0 or i == 0:
                result.append(f"{size[i]} {size[i+1]} {size[i+2]}")
    result = "\n".join(result)
    return result
            
def make_time():
    def getsize(font, text):
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top

    img = Image.open("today_time.png")

    f_s = 60
    font = ImageFont.truetype("KHNPHDotfR.otf", f_s, encoding="UTF-8")

    text = ""

    date = (datetime.now()).strftime("%m월 %d일")
    # date = (datetime.now() + timedelta(days=1)).strftime("%m월 %d일")
    try: text = get_time(date)
    except: raise(NoTimeError)

    # meals = meal[date]
    times = text

    tw, th = getsize(font, text)
    draw = ImageDraw.Draw(img)
    # (int(w/2)-tw/2, int(h/2)-int(font.size/2))
    # 384654
    # draw.text((512, 420), text, font=font, fill="#97BECF", align="center", anchor="ms")
    
    h = 210
    text = str(text).split("\n")
    for i in text:
        draw.text((350, h), i, font=font, fill="black", align="left")
        h += 210
    # draw.text((512, 420), text, font=font, fill="black", align="center", anchor="ms")
    ra = random.randint(10000, 99999)
    name = f"{date.replace(' ', '').replace('월', '').replace('일', '')}{ra}"
    img.save(f"C:/xampp/htdocs/images/times/{name}.png")
    img.save(f"C:/Users/Administrator/Desktop/meal_system/times/{name}.png")

    img2 = Image.open(f"background33.png")
    img3 = Image.open(f"C:/Users/Administrator/Desktop/meal_system/times/{name}.png")
    img2.paste(img3, box=(0, 512))
    # img2.save("test.png")
    img2.save(f"C:/xampp/htdocs/images/times/8888{name}.png")
    img2.save(f"C:/Users/Administrator/Desktop/meal_system/times/8888{name}.png")
    return date, name, times