import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time

API_KEY = "tAa+IHbWJZWTpatZo2Yujio/4JUEYL14nBSAhWDuiJnERdfDl2p/peXDw/BQJZEVUoCxWugMKH1wyRr2qKcuMQ=="
API_URL = "http://apis.data.go.kr/1390802/AgriFood/FdFoodImage/getKoreanFoodFdFoodImageList"

def fetch_food_data_xml(start_page=149, page_interval=1, count=20, page_size=20):
    all_items = []
    unique_keys = set()  # (식재료명, 식품분류) 중복 제거용

    for i in range(count):
        page = start_page + i * page_interval
        params = {
            "serviceKey": API_KEY,
            "service_Type": "xml",
            "Page_No": str(page),
            "Page_Size": str(page_size),
            "food_Name": ""
        }

        try:
            res = requests.get(API_URL, params=params, timeout=60)
            print(f"📡 Page {page} 요청 중... URL: {res.url}")

            root = ET.fromstring(res.content)
            items = root.findall(".//item")

            if not items:
                print(f"⚠️ Page {page}: 데이터 없음")
                continue

            for item in items:
                food = item.find(".//food")
                if food is None:
                    continue

                name = food.findtext("food_Nm", default="").strip()
                group = food.findtext("nation_Std_Food_Grupp_Code_Nm", default="").strip()

                key = (name, group)
                #if key in unique_keys:
                #    continue  # 중복이면 스킵
                unique_keys.add(key)

                all_items.append({
                    "식재료명": name,
                    "식품분류": group,
                    "음식대분류": item.findtext("upper_Fd_Grupp_Nm", default=""),
                    "음식중분류": item.findtext("fd_Grupp_Nm", default=""),
                    "포함된음식": item.findtext("fd_Nm", default=""),
                    "식품이미지URL": food.findtext("food_Image_Address", default=""),
                    "음식이미지URL": item.findtext("image_Address", default="")
                })

            print(f"✅ Page {page} 수집 완료 ({len(items)}건, 누적: {len(all_items)}건)")
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Page {page} 오류: {e}")
            continue

    return all_items

def save_to_csv(data, filename="ingredients_unique_1000.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n📁 저장 완료: {filename} (총 {len(df)}건)")

if __name__ == "__main__":
    result = fetch_food_data_xml()
    save_to_csv(result)
