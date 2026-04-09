import json
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).resolve().parent
api_products_path = base_path / "api_products.json"
site_path = base_path.parent / "site" / "deals.json"

with open(api_products_path, "r", encoding="utf-8") as f:
    api_products = json.load(f)

deals = []

for idx, item in enumerate(api_products, start=1):
    deals.append({
        "id": item.get("id", idx),
        "title": item.get("title", "상품명 없음"),
        "price": item.get("price", "가격 미정"),
        "category": item.get("category", "기타"),
        "image": item.get("image", ""),
        "link": item.get("link", ""),
        "badge": item.get("badge", "추천"),
        "date": datetime.now().strftime("%Y-%m-%d")
    })

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(deals, f, ensure_ascii=False, indent=2)

print("API용 deals.json 저장 완료")
print(site_path)
