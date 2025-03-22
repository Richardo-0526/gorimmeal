import make_meal, week_make_meal, time, requests, json, configparser as cp, datetime, make_time

config = cp.ConfigParser()
config.read('config.ini')

# access_token = config["facebook"]["access_token"]

# post_url = 'https://graph.facebook.com/v19.0/{}/media'.format(config["instagram"]["ig_user_id"])

# payload = {
#     'access_token': access_token,
#     'caption': f"2025학년도 대학수학능력시험",
#     'image_url': f"https://www.richardo.net/images/gorim_meal_suneng.png"
# }

# r = requests.post(post_url, data=payload)

# print(r.text)

# result = json.loads(r.text)

# if 'id' in result: creation_id = result['id']

# second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(config["instagram"]["ig_user_id"])
# second_payload = {
#     'creation_id': creation_id,
#     'access_token': access_token
# }

# try:
#     r = requests.post(second_url, data=second_payload)
#     print("인스타그램 포스팅 완료")
#     print(r.text)
# except Exception as e:
#     print("에러 발생" + e)

# exit()

# ------------------------

week = False
try: date = make_meal.make_meal()
except make_meal.NoMealError:
    day = datetime.datetime.now().weekday()
    if day == 6:
        date = week_make_meal.make_meal_week()
        week = True
        if len(date[1]) == 0: exit("급식 정보 없음")
    else: exit("급식 정보 없음")

# 원래 config 있는 곳



access_token = config["facebook"]["access_token"]

post_url = 'https://graph.facebook.com/v19.0/{}/media'.format(config["instagram"]["ig_user_id"])

if week:
    creation_id = []

    payload = {
        'access_token': access_token,
        'is_carousel_item': True,
        'image_url': f"https://www.richardo.net/images/week_meals/{date[0][0]}.png"
    }

    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result: creation_id.append(result['id'])

    for i in date[1]:
        payload = {
            'access_token': access_token,
            'is_carousel_item': True,
            # 'caption': f"🥣 고림고등학교 이번주의 급식 정보! ({date[0][1]})\n\n고림고등학교 급식을 팔로우 하시면 매일 아침 6시에 업로드되는 급식 정보를 확인하실 수 있습니다!\n#고림고등학교 #급식",
            'image_url': f"https://www.richardo.net/images/week_meals/{i[1]}.png"
        }

        r = requests.post(post_url, data=payload)
        print(r.text)
        result = json.loads(r.text)
        if 'id' in result: creation_id.append(result['id'])

    print(creation_id)

    payload = {
        'access_token': access_token,
        'media_type': 'CAROUSEL',
        'caption': f"🥣 고림고등학교 이번주의 급식 정보! {date[0][1]}\n\n📢 고림고등학교 급식을 팔로우 하시면 매일 아침 6시에 업로드되는 급식 정보를 확인하실 수 있습니다!\n#고림고등학교 #급식",
        'children': f','.join(creation_id)
    }

    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    # if 'id' in result: creation_id.append(result['id'])
    if 'id' in result: creation_id = result['id']

    second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(config["instagram"]["ig_user_id"])
    second_payload = {
        'creation_id': creation_id,
        'access_token': access_token
    }

    try:
        r = requests.post(second_url, data=second_payload)
        print("인스타그램 포스팅 완료")
        print(r.text)
    except Exception as e:
        print("에러 발생" + e)

    exit()

# ---------

no_time = False
try: times = make_time.make_time()
except make_time.NoTimeError: no_time = True

if no_time:
    payload = {
        'access_token': access_token,
        'caption': f"🥣 고림고등학교 {date[0]} 급식 정보\n\n----------------\n{date[2]}\n----------------\n\n📢 고림고등학교 급식을 팔로우 하시면 매일 아침 6시에 업로드되는 급식 정보를 확인하실 수 있습니다!\n#고림고등학교 #급식",
        'image_url': f"https://www.richardo.net/images/meal/{date[1]}.png"
    }

    payload_story = {
        'access_token': access_token,
        'media_type': 'STORIES',
        'image_url': f"https://www.richardo.net/images/meal/8888{date[1]}.png"
    }

    r = requests.post(post_url, data=payload)
    r2 = requests.post(post_url, data=payload_story)
    print(r.text)
    print(r2.text)
    result = json.loads(r.text)
    result2 = json.loads(r2.text)
    if 'id' in result: creation_id = result['id']
    if 'id' in result: creation_id2 = result2['id']

    second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(config["instagram"]["ig_user_id"])
    second_payload = {
        'creation_id': creation_id,
        'access_token': access_token
    }

    second_payload_story = {
        'creation_id': creation_id2,
        'access_token': access_token
    }

    try:
        r = requests.post(second_url, data=second_payload)
        r2 = requests.post(second_url, data=second_payload_story)
        print("인스타그램 포스팅 완료")
        print(r.text)
        print(r2.text)
    except Exception as e:
        print("에러 발생" + e)
    
    exit()

creation_id = []

payload = {
    'access_token': access_token,
    # 'caption': f"🥣 고림고등학교 {date[0]} 급식 정보\n\n----------------\n{date[2]}\n----------------\n\n고림고등학교 급식을 팔로우 하시면 매일 아침 6시에 업로드되는 급식 정보를 확인하실 수 있습니다!\n#고림고등학교 #급식",
    'is_carousel_item': True,
    'image_url': f"https://www.richardo.net/images/meal/{date[1]}.png"
}

r = requests.post(post_url, data=payload)
print(r.text)
result = json.loads(r.text)
if 'id' in result: creation_id.append(result['id'])

payload = {
    'access_token': access_token,
    'is_carousel_item': True,
    'image_url': f"https://www.richardo.net/images/times/{times[1]}.png"
}

r = requests.post(post_url, data=payload)
print(r.text)
result = json.loads(r.text)
if 'id' in result: creation_id.append(result['id'])

# -------------

payload = {
    'access_token': access_token,
    'media_type': 'CAROUSEL',
    'caption': f"🥣 고림고등학교 {date[0]} 급식 정보\n\n----------------\n{date[2]}\n----------------\n\n📢 고림고등학교 급식을 팔로우 하시면 매일 아침 6시에 업로드되는 급식 정보를 확인하실 수 있습니다!\n#고림고등학교 #급식",
    'children': f','.join(creation_id)
}

payload_story = {
    'access_token': access_token,
    'media_type': 'STORIES',
    'image_url': f"https://www.richardo.net/images/meal/8888{date[1]}.png"
}

payload_story_2 = {
    'access_token': access_token,
    'media_type': 'STORIES',
    'image_url': f"https://www.richardo.net/images/times/8888{times[1]}.png"
}

r = requests.post(post_url, data=payload)
r2 = requests.post(post_url, data=payload_story)
r3 = requests.post(post_url, data=payload_story_2)
print(r.text)
print(r2.text)
print(r3.text)
result = json.loads(r.text)
result2 = json.loads(r2.text)
result3 = json.loads(r3.text)
# if 'id' in result: creation_id.append(result['id'])
if 'id' in result: creation_id = result['id']
if 'id' in result2: creation_id2 = result2['id']
if 'id' in result3: creation_id3 = result3['id']

second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(config["instagram"]["ig_user_id"])
second_payload = {
    'creation_id': creation_id,
    'access_token': access_token
}

second_payload_story = {
    'creation_id': creation_id2,
    'access_token': access_token
}

second_payload_story_2 = {
    'creation_id': creation_id3,
    'access_token': access_token
}


try:
    r = requests.post(second_url, data=second_payload)
    r2 = requests.post(second_url, data=second_payload_story)
    r3 = requests.post(second_url, data=second_payload_story_2)
    print("인스타그램 포스팅 완료")
    print(r.text)
    print(r2.text)
    print(r3.text)
except Exception as e:
    print("에러 발생" + e)

exit()

