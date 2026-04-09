import json
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

base_path = Path(__file__).resolve().parent
products_path = base_path / "products.json"
site_path = base_path.parent / "site" / "deals.json"

with open(products_path, "r", encoding="utf-8") as f:
    product_links = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0"
}

deals = []

for item in product_links:
    title = item.get("manual_title", "상품명 없음")
    image = item.get("manual_image", "").strip()

    if not image:
        image = f"https://picsum.photos/400?random={item['id']}"

    try:
        response = requests.get(item["url"], headers=headers, timeout=15)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        og_title = soup.find("meta", property="og:title")
        og_image = soup.find("meta", property="og:image")

        if og_title and og_title.get("content"):
            auto_title = og_title.get("content").strip()
            if auto_title and "불러오기 실패" not in auto_title:
                title = auto_title

        if og_image and og_image.get("content"):
            auto_image = og_image.get("content").strip()
            if auto_image:
                image = auto_image

    except Exception as e:
        print(f"{item['id']}번 상품 수집 실패:", e)

    deals.append({
        "id": item["id"],
        "title": title,
        "price": item["price"],
        "category": item["category"],
        "image": image,
        "link": item["url"],
        "badge": item["badge"],
        "date": datetime.now().strftime("%Y-%m-%d")
    })

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(deals, f, ensure_ascii=False, indent=2)

print("deals.json 저장 완료")
print(site_path)