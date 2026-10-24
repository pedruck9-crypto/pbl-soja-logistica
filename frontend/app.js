const filters = [...document.querySelectorAll(".filter-chip")];
const cards = [...document.querySelectorAll(".data-card")];
const searchInput = document.querySelector("#search-input");
const emptyState = document.querySelector("#empty-state");
let selectedFilter = "all";

function applyFilters() {
  const query = searchInput.value.trim().toLocaleLowerCase("pt-BR");
  let visibleCount = 0;

  for (const card of cards) {
    const matchesFilter = selectedFilter === "all" || card.dataset.status === selectedFilter;
    const searchable = `${card.dataset.search} ${card.textContent}`.toLocaleLowerCase("pt-BR");
    const matchesSearch = !query || searchable.includes(query);
    const visible = matchesFilter && matchesSearch;
    card.hidden = !visible;
    if (visible) visibleCount += 1;
  }

  emptyState.hidden = visibleCount > 0;
}

filters.forEach((button) => {
  button.addEventListener("click", () => {
    selectedFilter = button.dataset.filter;
    filters.forEach((item) => {
      const active = item === button;
      item.classList.toggle("selected", active);
      item.setAttribute("aria-pressed", String(active));
    });
    applyFilters();
  });
});

searchInput.addEventListener("input", applyFilters);

const navLinks = [...document.querySelectorAll(".nav-link")];
const navSections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    const current = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!current) return;
    navLinks.forEach((link) => {
      const active = link.getAttribute("href") === `#${current.target.id}`;
      link.classList.toggle("active", active);
    });
  }, { rootMargin: "-20% 0px -65% 0px", threshold: [0, 0.25, 0.5] });

  navSections.forEach((section) => observer.observe(section));
}
