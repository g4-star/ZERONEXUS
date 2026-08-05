/* ============================================================
 * ZeroNexus Dashboard
 * ============================================================ */

window.ZeroNexus = window.ZeroNexus || {};

(function () {

    "use strict";

    /* ============================================================
     * Sidebar Toggle
     * ============================================================ */

    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");
    const app = document.querySelector(".app");

    if (menuBtn && sidebar) {

        menuBtn.addEventListener("click", function () {

            if (window.innerWidth <= 992) {

                sidebar.classList.toggle("open");

            } else if (app) {

                app.classList.toggle("sidebar-collapsed");

            }

        });

        document.addEventListener("click", function (e) {

            if (
                window.innerWidth <= 992 &&
                sidebar.classList.contains("open") &&
                !sidebar.contains(e.target) &&
                !menuBtn.contains(e.target)
            ) {

                sidebar.classList.remove("open");

            }

        });

    }

    /* ============================================================
     * Task Toggle
     * ============================================================ */

    window.toggleTask = function (item) {

        if (item) {

            item.classList.toggle("done");

        }

    };

    /* ============================================================
     * Toast Notification
     * ============================================================ */

    const toastEl = document.getElementById("toast");

    let toastTimer = null;

    window.ZeroNexus.showToast = function (message, isError = false) {

        if (!toastEl) return;

        toastEl.textContent = message;

        toastEl.style.borderColor = isError
            ? "rgba(239,68,68,.6)"
            : "rgba(139,92,246,.5)";

        toastEl.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(function () {

            toastEl.classList.remove("show");

        }, 2500);

    };

    /* ============================================================
     * Animate Progress Rings
     * ============================================================ */

    function animateRings() {

        const radius = 34;

        const circumference = 2 * Math.PI * radius;

        document.querySelectorAll(".ring-fg").forEach(function (ring) {

            const percent = Math.max(
                0,
                Math.min(
                    100,
                    parseInt(ring.dataset.pct || 0)
                )
            );

            ring.style.strokeDasharray = circumference;

            ring.style.strokeDashoffset =
                circumference -
                (circumference * percent) / 100;

        });

    }

    /* ============================================================
     * Animate Progress Bars
     * ============================================================ */

    function animateBars() {

        document.querySelectorAll(".bar-fill").forEach(function (bar) {

            const width = Math.max(
                0,
                Math.min(
                    100,
                    parseInt(bar.dataset.w || 0)
                )
            );

            bar.style.width = width + "%";

        });

    }

    /* ============================================================
     * Animate Completion Bars
     * ============================================================ */

    function animateCompletionBars() {

        document.querySelectorAll(".comp-fill").forEach(function (bar) {

            const width = Math.max(
                0,
                Math.min(
                    100,
                    parseInt(bar.dataset.w || 0)
                )
            );

            bar.style.width = width + "%";

        });

    }

    /* ============================================================
     * Initialize Dashboard
     * ============================================================ */

    window.addEventListener("load", function () {

        setTimeout(function () {

            animateRings();

            animateBars();

            animateCompletionBars();

        }, 100);

    });

})();