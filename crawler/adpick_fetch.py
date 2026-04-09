import json
import requests
from pathlib import Path

# 애드픽 추천상품 API URL 넣기
ADPICK_URL = "https://adpick.co.kr/apis/sdk_shopping.php?affid=11b2e6"

base_path = Path(__file__).resolve().parent
api_products_path = base_path / "api_products.json"

response = requests.get(ADPICK_URL, timeout=20)
response.raise_for_status()
data = response.json()

# 응답이 dict일 수도 있고 list일 수도 있어서 둘 다 처리
if isinstance(data, dict):
    items = data.get("list", [])
elif isinstance(data, list):
    items = data
else:
    items = []

converted = []

for idx, item in enumerate(items, start=1):
    converted.append({
        "id": idx,
        "title": item.get("product_name", "상품명 없음"),
        "price": str(item.get("price_sale", "")),
        "category": item.get("mall", "기타"),
        "image": item.get("photo", ""),
        "link": item.get("buyurl", ""),
        "badge": "추천"
    })

with open(api_products_path, "w", encoding="utf-8") as f:
    json.dump(converted, f, ensure_ascii=False, indent=2)

print("애드픽 API -> api_products.json 저장 완료")
print(api_products_path)
print(f"상품 개수: {len(converted)}")