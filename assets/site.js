/* =========================================================
   Rackets & Rhythms — site config + behaviour
   ---------------------------------------------------------
   EDIT THIS SECTION to update links, sessions and events.
   Checkout links: paste a Stripe Payment Link (or Eventbrite,
   Fatsoma, Ticket Tailor, etc.) for each product. While a link
   is empty, the button shows a friendly "coming soon" message.
   ========================================================= */
const CONFIG = {
  checkout: {
    saturdaysPass: "",   // e.g. "https://buy.stripe.com/xxxx"  (£8 one-off)
    membership: "",      // e.g. "https://buy.stripe.com/yyyy"  (£20/month subscription)
  },

  social: {
    instagram: "",       // e.g. "https://instagram.com/racketsandrhythms"
    tiktok: "",
  },

  // R&R Saturdays — each one is bookable with the £8 pass.
  saturdays: [
    { date: "2026-11-14", time: "12:00 – 15:00", place: "Danson Park, Welling" },
    { date: "2026-11-21", time: "12:00 – 15:00", place: "Danson Park, Welling" },
    { date: "2026-11-28", time: "12:00 – 15:00", place: "Danson Park, Welling" },
  ],

  // Separate events — PLACEHOLDERS: replace with your real events.
  events: [
    {
      title: "Doubles Showdown",
      date: "2026-12-05",
      time: "12:00 – 16:00",
      place: "Danson Park, Welling",
      blurb: "Pick a partner, run the bracket. DJ on deck all afternoon.",
      price: 15, memberPrice: 10,
      link: "",
    },
    {
      title: "Rackets After Dark",
      date: "2026-12-12",
      time: "18:00 – 22:00",
      place: "Venue TBC",
      blurb: "End-of-year social. Food, music and the R&R family under one roof.",
      price: 20, memberPrice: 15,
      link: "",
    },
    {
      title: "New Year Reset Session",
      date: "2027-01-09",
      time: "11:00 – 13:00",
      place: "Danson Park, Welling",
      blurb: "Kick off the year with drills, conditioning and a cool-down playlist.",
      price: 10, memberPrice: 6,
      link: "",
    },
  ],
};

/* ========================================================= */

(() => {
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const parse = s => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const ord = n => (n % 100 >= 11 && n % 100 <= 13) ? "th" : ({ 1: "st", 2: "nd", 3: "rd" }[n % 10] || "th");
  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---- checkout ----
  const modal = document.getElementById("modal");
  function checkout(url, name) {
    if (url) { window.open(url, "_blank", "noopener"); return; }
    document.getElementById("modalTitle").textContent = name;
    document.getElementById("modalBody").textContent =
      "Online checkout is opening soon. In the meantime, drop us a DM on Instagram to secure your spot.";
    modal.showModal();
  }
  const NAMES = { saturdaysPass: "R&R Saturdays Pass", membership: "R&R Membership" };
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-buy]");
    if (b) checkout(CONFIG.checkout[b.dataset.buy], NAMES[b.dataset.buy]);
    const ev = e.target.closest("[data-event]");
    if (ev) { const x = CONFIG.events[+ev.dataset.event]; checkout(x.link, x.title); }
  });

  // ---- Saturdays tracklist ----
  document.getElementById("tracklist").innerHTML = CONFIG.saturdays.map((s, i) => {
    const d = parse(s.date), past = d < today, n = d.getDate();
    return `<li class="track${past ? " is-past" : ""}">
      <span class="track__n">${String(i + 1).padStart(2, "0")}</span>
      <div>
        <div class="track__date">${DAYS[d.getDay()]} ${n}<sup>${ord(n)}</sup> ${MONTHS[d.getMonth()]}</div>
        <div class="track__meta">${esc(s.time)} · ${esc(s.place)}</div>
      </div>
      <button class="btn btn--blue btn--sm" data-buy="saturdaysPass" ${past ? "disabled" : ""}>${past ? "Done" : "Book · £8"}</button>
    </li>`;
  }).join("");

  // ---- events ----
  const upcoming = CONFIG.events.map((e, i) => ({ ...e, i })).filter(e => parse(e.date) >= today);
  document.getElementById("eventGrid").innerHTML = upcoming.length ? upcoming.map(e => {
    const d = parse(e.date);
    return `<article class="event reveal">
      <div class="event__top">
        <div class="event__date"><small>${DAYS[d.getDay()]}</small>${d.getDate()} ${MONTHS[d.getMonth()]}</div>
      </div>
      <div class="event__body">
        <h3>${esc(e.title)}</h3>
        <p>${esc(e.time)} · ${esc(e.place)}</p>
        <p>${esc(e.blurb)}</p>
        <div class="event__foot">
          <div class="event__price">£${e.price}${e.memberPrice != null ? `<small>Members £${e.memberPrice}</small>` : ""}</div>
          <button class="btn btn--green btn--sm" data-event="${e.i}">Get tickets</button>
        </div>
      </div>
    </article>`;
  }).join("") : `<p class="note">New events dropping soon. Watch this space.</p>`;

  // ---- socials / footer ----
  for (const [id, key] of [["instaLink", "instagram"], ["tiktokLink", "tiktok"]]) {
    const a = document.getElementById(id);
    if (CONFIG.social[key]) a.href = CONFIG.social[key]; else a.removeAttribute("href");
  }
  document.getElementById("year").textContent = new Date().getFullYear();

  // ---- reveal on scroll ----
  document.querySelectorAll(".price-card, .track, .pillar, .ph, .flyer, .section__head").forEach(el => el.classList.add("reveal"));
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));
})();
