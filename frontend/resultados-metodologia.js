const priceRange = document.querySelector("#price-range");

if (priceRange) {
  const priceOutput = document.querySelector("#price-output");
  const quantityOutput = document.querySelector("#quantity-output");
  const revenueOutput = document.querySelector("#revenue-output");
  const costOutput = document.querySelector("#cost-output");
  const profitOutput = document.querySelector("#profit-output");
  const integer = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
  const money = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

  const millions = (value) => `${money.format(value / 1_000_000)} mi`;

  const updateProfitModel = () => {
    const price = Number(priceRange.value);
    const quantity = Math.max(0, (price - 180) / 0.0012);
    const revenue = price * quantity;
    const cost = 5_000_000 + 180 * quantity + 0.0006 * quantity ** 2;
    const profit = revenue - cost;

    priceOutput.textContent = `${money.format(price)}/t`;
    quantityOutput.textContent = `${integer.format(quantity)} t`;
    revenueOutput.textContent = millions(revenue);
    costOutput.textContent = millions(cost);
    profitOutput.textContent = millions(profit);
  };

  priceRange.addEventListener("input", updateProfitModel);
  updateProfitModel();
}
