const dictionaryFilter = document.querySelector("#dictionary-filter");
const dictionaryCards = [...document.querySelectorAll("#dictionary-grid article")];

if (dictionaryFilter) {
  dictionaryFilter.addEventListener("input", () => {
    const term = dictionaryFilter.value.trim().toLocaleLowerCase("pt-BR");
    dictionaryCards.forEach((card) => {
      const content = `${card.dataset.terms || ""} ${card.textContent}`.toLocaleLowerCase("pt-BR");
      card.hidden = term !== "" && !content.includes(term);
    });
  });
}
