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

function renderCategoryButtons() {
  const categories = ["전체", ...new Set(allDeals.map(deal => deal.category))];

  categoryButtons.innerHTML = categories.map(category => `
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
      : allDeals.filter(deal => deal.category === selectedCategory);

  dealList.innerHTML = filteredDeals.map(deal => `
    <div class="deal-card">
      <img src="${deal.image}" alt="${deal.title}" />
      <div class="deal-content">
        <div class="badge">${deal.badge}</div>
        <div class="category">${deal.category}</div>
        <div class="title">${deal.title}</div>
        <div class="price">${deal.price}</div>
        <div class="date">${deal.date}</div>
        <a class="buy-button" href="${deal.link}" target="_blank">구매하러 가기</a>
      </div>
    </div>
  `).join("");
}

loadDeals();