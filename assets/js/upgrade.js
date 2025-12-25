(function () {
  const revealEls = document.querySelectorAll(
    "section, .box-shadow-full, .service-box, .work-box, .card, .card-blog"
  );
  revealEls.forEach(el => el.classList.add("tw-reveal"));

  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add("tw-in");
    });
  }, { threshold: 0.12 });

  revealEls.forEach(el => io.observe(el));

  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("a[href^='#']");
    if (!a) return;

    const id = a.getAttribute("href");
    if (!id || id === "#") return;

    const target = document.querySelector(id);
    if (!target) return;

    ev.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
