/*
==========================================================
ZeroNexus Progress System
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeProgressRings();
    initializeProgressBars();
    animateXP();
    animateCompletion();

});

/* ====================================================== */

function initializeProgressRings() {

    document.querySelectorAll(".progress-ring").forEach(ring => {

        const circle = ring.querySelector(".progress-ring-circle");

        if (!circle) return;

        const progress = parseFloat(ring.dataset.progress || 0);

        const radius = parseFloat(circle.getAttribute("r"));

        const circumference = 2 * Math.PI * radius;

        circle.style.strokeDasharray = circumference;

        const offset = circumference - (progress / 100) * circumference;

        circle.style.strokeDashoffset = circumference;

        requestAnimationFrame(() => {

            circle.style.transition = "stroke-dashoffset 1.8s ease";
            circle.style.strokeDashoffset = offset;

        });

    });

}

/* ====================================================== */

function initializeProgressBars() {

    document.querySelectorAll(".animated-progress").forEach(bar => {

        const value = bar.dataset.value || 0;

        bar.style.width = "0%";

        setTimeout(() => {

            bar.style.transition = "width 1.5s ease";
            bar.style.width = value + "%";

        }, 200);

    });

}

/* ====================================================== */

function animateXP() {

    document.querySelectorAll(".xp-counter").forEach(counter => {

        const target = parseInt(counter.dataset.target || 0);

        let value = 0;

        const timer = setInterval(() => {

            value += Math.ceil(target / 60);

            if (value >= target) {

                value = target;
                clearInterval(timer);

            }

            counter.textContent = value.toLocaleString();

        }, 20);

    });

}

/* ====================================================== */

function animateCompletion() {

    document.querySelectorAll(".completion-percent").forEach(counter => {

        const target = parseInt(counter.dataset.target || 0);

        let current = 0;

        const interval = setInterval(() => {

            current++;

            counter.innerHTML = current + "%";

            if (current >= target) {

                clearInterval(interval);

            }

        }, 15);

    });

}