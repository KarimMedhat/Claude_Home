(function () {
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      const expanded = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!expanded));
      navMenu.classList.toggle("hidden");
      navMenu.classList.toggle("flex");
    });

    navMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (window.matchMedia("(max-width: 1023px)").matches) {
          navMenu.classList.add("hidden");
          navMenu.classList.remove("flex");
          menuToggle.setAttribute("aria-expanded", "false");
        }
      });
    });

    window.addEventListener("resize", () => {
      if (window.matchMedia("(min-width: 1024px)").matches) {
        navMenu.classList.remove("hidden");
        navMenu.classList.add("flex");
      } else if (menuToggle.getAttribute("aria-expanded") !== "true") {
        navMenu.classList.add("hidden");
        navMenu.classList.remove("flex");
      }
    });
  }

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!prefersReducedMotion) {
    const revealEls = document.querySelectorAll("[data-reveal]");
    revealEls.forEach((el) => {
      el.classList.add("opacity-0", "translate-y-8");
      el.style.transition = "opacity 0.75s cubic-bezier(0.22, 1, 0.36, 1), transform 0.75s cubic-bezier(0.22, 1, 0.36, 1)";
      const delay = el.getAttribute("data-delay");
      if (delay) el.style.transitionDelay = `${parseInt(delay, 10)}ms`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          el.classList.remove("opacity-0", "translate-y-8");
          el.classList.add("opacity-100", "translate-y-0");
          observer.unobserve(el);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    revealEls.forEach((el) => observer.observe(el));
  } else {
    document.querySelectorAll("[data-reveal]").forEach((el) => {
      el.classList.remove("opacity-0", "translate-y-8");
    });
  }
})();
