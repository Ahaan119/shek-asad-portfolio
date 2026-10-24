(function () {
  "use strict";

  // Reveal-on-scroll (the .js class is set in <head>, so content stays visible without JavaScript)
  var els = document.querySelectorAll("[data-reveal], .stamp");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.18 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  // Work page: filter the "ad account" rows by the symptom
  var chips = document.querySelectorAll("[data-filter]");
  var rows = document.querySelectorAll("[data-sym]");
  var counter = document.getElementById("count");
  if (chips.length && rows.length) {
    var apply = function (key) {
      var shown = 0;
      rows.forEach(function (r) {
        var on = key === "all" || r.getAttribute("data-sym").split(" ").indexOf(key) > -1;
        r.hidden = !on;
        if (on) shown++;
      });
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === key)); });
      if (counter) counter.textContent = "Showing " + shown + " of " + rows.length + " campaigns";
    };
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var k = c.getAttribute("data-filter");
        history.replaceState(null, "", k === "all" ? location.pathname : "#sym-" + k);
        apply(k);
      });
    });
    var fromHash = function () {
      var m = location.hash.match(/^#sym-(.+)$/);
      apply(m ? m[1] : "all");
    };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }
})();
