// ChitwanFit — small interactions only (motion budget: 1 scroll effect + the theme toggle).

// ---- Scroll reveal: sections get a subtle fade-up when they scroll into view.
const revealItems = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

revealItems.forEach((item) => observer.observe(item));

// ---- Theme toggle: switch light/dark and remember the choice.
const toggleButton = document.getElementById("theme-toggle");
if (toggleButton) {
  const applyThemeButton = () => {
    const theme = document.documentElement.getAttribute("data-theme") || "light";
    toggleButton.textContent = theme === "light" ? "☾" : "☀";
  };

  toggleButton.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("chitwanfit-theme", next);
    applyThemeButton();
  });

  applyThemeButton();
}