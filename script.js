const dealList = document.getElementById("deal-list");

async function loadDeals() {
  try {
    const response = await fetch("./deals.json");

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const deals = await response.json();

    dealList.innerHTML = deals.map(deal => `
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
  } catch (error) {
    dealList.innerHTML = `<p>상품을 불러오지 못했어요. (${error.message})</p>`;
    console.error(error);
  }
}

loadDeals();