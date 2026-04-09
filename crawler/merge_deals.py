import json
from pathlib import Path
from datetime import datetime

base_path = Path(__file__).resolve().parent
site_path = base_path.parent / "site" / "deals.json"
root_path = base_path.parent / "deals.json"

sources = [
    base_path / "api_products.json",
    base_path / "products.json"
]

rules_path = base_path / "rules.json"

with open(rules_path, "r", encoding="utf-8") as f:
    rules = json.load(f)

default_badge = rules.get("default_badge", "추천")
special_badges = rules.get("special_badges", {})
exclude_if_no_price = rules.get("exclude_if_no_price", True)
sort_by_latest = rules.get("sort_by_latest", True)

merged = []
seen_links = set()

def decide_badge(item):
    title = (item.get("manual_title") or item.get("title") or "").strip()
    badge = (item.get("badge") or "").strip()

    if badge:
        return badge

    for keyword, mapped_badge in special_badges.items():
        if keyword in title:
            return mapped_badge

    return default_badge

for source in sources:
    if source.exists():
        with open(source, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:
            link = item.get("url") or item.get("link") or ""
            price = (item.get("price") or "").strip()

            if exclude_if_no_price and not price:
                continue

            if link and link not in seen_links:
                seen_links.add(link)

                merged.append({
                    "id": item.get("id", len(merged) + 1),
                    "title": item.get("manual_title") or item.get("title", "상품명 없음"),
                    "price": price if price else "가격 미정",
                    "category": item.get("category", "기타"),
                    "image": item.get("manual_image") or item.get("image", ""),
                    "link": item.get("url") or item.get("link", ""),
                    "badge": decide_badge(item),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

if sort_by_latest:
    merged = list(reversed(merged))

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

with open(root_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("통합 deals.json 저장 완료")
print(site_path)
print(root_path)