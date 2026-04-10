const dealList = document.getElementById("deal-list");
const categoryButtons = document.getElementById("category-buttons");

let allDeals = [];
let selectedCategory = "전체";

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
  const badge = (deal.badge || "").trim();

  if (badge === "핫딜") return "핫딜";
  if (badge === "추천") return "추천";

  return "기타";
}

function renderCategoryButtons() {
  const tabs = ["전체", "추천", "핫딜"];

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
  const filteredDeals =
    selectedCategory === "전체"
      ? allDeals
      : allDeals.filter(deal => getTabName(deal) === selectedCategory);

  if (!filteredDeals.length) {
    dealList.innerHTML = `<p class="empty-message">${selectedCategory} 상품이 아직 없어요.</p>`;
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
        <div class="date">${deal.date || ""}</div>
        <a class="buy-button" href="${deal.link}" target="_blank">구매하러 가기</a>
      </div>
    </div>
  `).join("");
}

loadDeals();