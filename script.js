const dealList = document.getElementById("deal-list");
const categoryButtons = document.getElementById("category-buttons");
const searchInput = document.getElementById("search-input");
const sortSelect = document.getElementById("sort-select");

let allDeals = [];
let selectedCategory = "전체";
let searchKeyword = "";
let selectedSort = "latest";

async function loadDeals() {
  try {
    const response = await fetch("./deals.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const deals = await response.json();
    allDeals = deals;

    renderCategoryButtons();
    renderDeals();
  } catch (error) {
    dealList.innerHTML = `<p>상품을 불러오지 못했어요. (${error.message})</p>`;
    console.error(error);
  }
}

function formatPrice(price) {
  if (!price) return "가격 미정";

  const raw = String(price).replace(/[^\d]/g, "");
  if (!raw) return String(price);

  return Number(raw).toLocaleString("ko-KR") + "원";
}

function getTabName(deal) {
  const sourceType = (deal.source_type || "").trim();

  if (sourceType === "추천") return "애드픽 추천";
  if (sourceType === "핫딜") return "애드픽 핫딜";
  if ((deal.source || "").trim() === "쿠팡") return "쿠팡";

  return "기타";
}

function renderCategoryButtons() {
  const tabs = ["전체", "애드픽 추천", "애드픽 핫딜", "쿠팡"];

  categoryButtons.innerHTML = tabs.map(category => `
    <button
      class="category-button ${category === selectedCategory ? "active" : ""}"
      data-category="${category}"
    >
      ${category}
    </button>
  `).join("");

  const buttons = document.querySelectorAll(".category-button");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      selectedCategory = button.dataset.category;
      renderCategoryButtons();
      renderDeals();
    });
  });
}

function renderDeals() {
  let filteredDeals =
    selectedCategory === "전체"
      ? [...allDeals]
      : allDeals.filter(deal => getTabName(deal) === selectedCategory);

  if (searchKeyword.trim()) {
    const keyword = searchKeyword.trim().toLowerCase();

    filteredDeals = filteredDeals.filter(deal => {
      const title = (deal.title || "").toLowerCase();
      const category = (deal.category || "").toLowerCase();
      const source = (deal.source || "").toLowerCase();

      return (
        title.includes(keyword) ||
        category.includes(keyword) ||
        source.includes(keyword)
      );
    });
  }

  if (selectedSort === "priceLow") {
    filteredDeals.sort((a, b) => {
      const priceA = Number(String(a.price || "").replace(/[^\d]/g, "")) || 0;
      const priceB = Number(String(b.price || "").replace(/[^\d]/g, "")) || 0;
      return priceA - priceB;
    });
  }

  if (selectedSort === "priceHigh") {
    filteredDeals.sort((a, b) => {
      const priceA = Number(String(a.price || "").replace(/[^\d]/g, "")) || 0;
      const priceB = Number(String(b.price || "").replace(/[^\d]/g, "")) || 0;
      return priceB - priceA;
    });
  }

  if (!filteredDeals.length) {
    dealList.innerHTML = `<p class="empty-message">조건에 맞는 상품이 아직 없어요.</p>`;
    return;
  }

  dealList.innerHTML = filteredDeals.map(deal => `
    <div class="deal-card">
      <img src="${deal.image}" alt="${deal.title}" />
      <div class="deal-content">
        <div class="badge">${deal.badge || "추천"}</div>
        <div class="category">${deal.category || "기타"}</div>
        <div class="title">${deal.title}</div>
        <div class="price">${formatPrice(deal.price)}</div>
        ${deal.commission ? `<div class="commission">커미션 ${deal.commission}</div>` : ""}
        <div class="date">${deal.date || ""}</div>
        <a class="buy-button" href="${deal.link}" target="_blank">구매하러 가기</a>
      </div>
    </div>
  `).join("");
}

if (searchInput) {
  searchInput.addEventListener("input", (e) => {
    searchKeyword = e.target.value;
    renderDeals();
  });
}

if (sortSelect) {
  sortSelect.addEventListener("change", (e) => {
    selectedSort = e.target.value;
    renderDeals();
  });
}

loadDeals();