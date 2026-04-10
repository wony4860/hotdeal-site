import json
import requests
from pathlib import Path

# 애드픽 핫딜 API URL 넣기
ADPICK_HOTDEAL_URL = "https://adpick.co.kr/apis/sdk_shopping_hotdeal.php?affid=11b2e6"

base_path = Path(__file__).resolve().parent
hotdeal_products_path = base_path / "api_hotdeals.json"
raw_path = base_path / "adpick_hotdeal_raw.json"

response = requests.get(ADPICK_HOTDEAL_URL, timeout=20)
response.raise_for_status()
data = response.json()

with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

items = []

if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
    items = data[0].get("list", [])
elif isinstance(data, dict):
    items = data.get("list", [])
else:
    items = []

converted = []

for idx, item in enumerate(items, start=1):
    converted.append({
    "id": idx,
    "title": item.get("product_name", "상품명 없음"),
    "price": item.get("price_sale", ""),
    "category": item.get("mall_name") or item.get("mall") or "핫딜",
    "image": item.get("photo", ""),
    "link": item.get("buyurl", ""),
    "badge": "핫딜",
    "source": "애드픽",
    "source_type": "핫딜",
    "commission": item.get("commission", "")
})

with open(hotdeal_products_path, "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)

print("애드픽 핫딜 API -> api_hotdeals.json 저장 완료")
print(hotdeal_products_path)
print(f"상품 개수: {len(converted)}")