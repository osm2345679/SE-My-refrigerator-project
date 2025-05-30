import pandas as pd
from duckduckgo_search import DDGS
import time

# CSV 불러오기
df = pd.read_csv("ingredients.csv")
df["new_image_url"] = None

# 유효한 이미지 필터 함수
def is_valid_food_image(url):
    blacklist = ["ytimg.com", "youtube", "blog", "naver.com", "pinterest", "tistory"]
    return not any(domain in url for domain in blacklist)

# 이미지 검색 함수
def get_image_url(query):
    with DDGS() as ddgs:
        results = ddgs.images(query + " 식재료 사진", max_results=5)
        for result in results:
            url = result["image"]
            if is_valid_food_image(url):
                return url
    return None

# 전체 식재료에 대해 검색
for idx, row in df.iterrows():
    name = row["식재료명"]
    print(f"🔍 검색 중: {name}")
    try:
        url = get_image_url(name)
        df.at[idx, "new_image_url"] = url
    except Exception as e:
        print(f"❌ 1차 실패: {name} - {e}")
        time.sleep(10)  # 1차 실패 후 기다림
        try:
            print(f"🔁 재시도 중: {name}")
            url = get_image_url(name)
            df.at[idx, "new_image_url"] = url
        except Exception as e2:
            print(f"⛔ 최종 실패: {name} - {e2}")
    time.sleep(5)  # 기본 대기 시간

# 결과 저장
df.to_csv("ingredients_with_new_images.csv", index=False)
print("✅ 저장 완료 → ingredients_with_new_images.csv")
