import json
from pathlib import Path

base_path = Path(__file__).resolve().parent
site_path = base_path.parent / "site" / "deals.json"

sources = [
    base_path / "products.json",
    base_path / "api_products.json"
]

merged = []
seen_links = set()

for source in sources:
    if source.exists():
        with open(source, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            link = item.get("url") or item.get("link") or ""
            if link and link not in seen_links:
                seen_links.add(link)

                merged.append({
                    "id": item.get("id", len(merged) + 1),
                    "title": item.get("manual_title") or item.get("title", "상품명 없음"),
                    "price": item.get("price", "가격 미정"),
                    "category": item.get("category", "기타"),
                    "image": item.get("manual_image") or item.get("image", ""),
                    "link": item.get("url") or item.get("link", ""),
                    "badge": item.get("badge", "추천"),
                    "date": item.get("date", "")
                })

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("통합 deals.json 저장 완료")
print(site_path)
