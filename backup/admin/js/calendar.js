/* ============================================================
 * ZeroNexus Calendar
 * Professional Calendar Widget
 * ============================================================ */

(function () {

    "use strict";

    if (!window.ZeroNexus) {
        console.warn("ZeroNexus popup system not loaded.");
        return;
    }

    const MONTHS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];

    const WEEKDAYS = [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ];

    const FALLBACK_EVENTS = {
        3: "Team Sync Meeting",
        7: "Project Review",
        12: "Cybersecurity Workshop",
        18: "Sprint Planning",
        25: "Deployment"
    };

    let currentDate = new Date();

    let selectedDay = new Date().getDate();

    function getEvents(backdrop) {

        const events = {};

        backdrop.querySelectorAll(".cal-event").forEach(event => {

            const day = event.querySelector(".ev-date b");
            const title = event.querySelector(".ev-main b");

            if (!day || !title) {
                return;
            }

            const number = parseInt(day.textContent.trim(), 10);

            if (!isNaN(number)) {
                events[number] = title.textContent.trim();
            }

        });

        return Object.keys(events).length
            ? events
            : FALLBACK_EVENTS;

    }

    function render(backdrop) {

        const grid = backdrop.querySelector("#calGrid");
        const label = backdrop.querySelector("#calLabel");

        if (!grid || !label) {
            return;
        }

        const year = currentDate.getFullYear();

        const month = currentDate.getMonth();

        label.textContent = MONTHS[month] + " " + year;

        const firstDay = new Date(year, month, 1).getDay();

        const daysInMonth = new Date(year, month + 1, 0).getDate();

        const previousMonthDays = new Date(year, month, 0).getDate();

        const today = new Date();

        const events = getEvents(backdrop);

        let html = "";

        WEEKDAYS.forEach(day => {

            html += `
                <div class="cal-dow">
                    ${day}
                </div>
            `;

        });

        for (let i = firstDay - 1; i >= 0; i--) {

            html += `
                <div class="cal-day other">
                    ${previousMonthDays - i}
                </div>
            `;

        }

        for (let day = 1; day <= daysInMonth; day++) {

            let classes = ["cal-day"];

            if (
                today.getFullYear() === year &&
                today.getMonth() === month &&
                today.getDate() === day
            ) {
                classes.push("today");
            }

            if (day === selectedDay) {
                classes.push("selected");
            }

            if (events[day]) {
                classes.push("has-event");
            }

            html += `
                <div
                    class="${classes.join(" ")}"
                    data-day="${day}"
                    title="${events[day] || ""}">
                    ${day}
                </div>
            `;

        }

        grid.innerHTML = html;

        grid.querySelectorAll(".cal-day:not(.other)").forEach(cell => {

            cell.addEventListener("click", function () {

                selectedDay = Number(this.dataset.day);

                render(backdrop);

                const info = backdrop.querySelector("#selectedEvent");

                if (!info) {
                    return;
                }

                if (events[selectedDay]) {

                    info.innerHTML = `
                        <strong>${MONTHS[month]} ${selectedDay}</strong><br>
                        ${events[selectedDay]}
                    `;

                } else {

                    info.innerHTML = `
                        <strong>${MONTHS[month]} ${selectedDay}</strong><br>
                        No events scheduled.
                    `;

                }

            });

        });

    }

    function bindNavigation(backdrop) {

        const prev = backdrop.querySelector("#calPrev");

        const next = backdrop.querySelector("#calNext");

        if (prev && !prev.dataset.bound) {

            prev.dataset.bound = "true";

            prev.addEventListener("click", function () {

                currentDate.setMonth(currentDate.getMonth() - 1);

                render(backdrop);

            });

        }

        if (next && !next.dataset.bound) {

            next.dataset.bound = "true";

            next.addEventListener("click", function () {

                currentDate.setMonth(currentDate.getMonth() + 1);

                render(backdrop);

            });

        }

    }

    window.ZeroNexus.registerModal("calendar", {

        onOpen(backdrop) {

            bindNavigation(backdrop);

            render(backdrop);

            const info = backdrop.querySelector("#selectedEvent");

            if (info) {

                info.innerHTML = `
                    <strong>Today</strong><br>
                    Select a date to view events.
                `;

            }

        }

    });

})();