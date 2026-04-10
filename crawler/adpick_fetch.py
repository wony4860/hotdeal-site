import json
import requests
from pathlib import Path

# 애드픽 추천상품 API URL 넣기
ADPICK_URL = "https://adpick.co.kr/apis/sdk_shopping.php?affid=11b2e6"

base_path = Path(__file__).resolve().parent
api_products_path = base_path / "api_products.json"
raw_path = base_path / "adpick_raw.json"

response = requests.get(ADPICK_URL, timeout=20)
response.raise_for_status()
data = response.json()

with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

items = []

# 애드픽 응답 구조 처리
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
    "category": item.get("mall_name") or item.get("mall") or "기타",
    "image": item.get("photo", ""),
    "link": item.get("buyurl", ""),
    "badge": "추천",
    "source": "애드픽",
    "source_type": "추천",
    "commission": item.get("commission", "")
})

with open(api_products_path, "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)

print("애드픽 API -> api_products.json 저장 완료")
print(api_products_path)
print(f"상품 개수: {len(converted)}")