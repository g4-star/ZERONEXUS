/* ============================================================
 * ZeroNexus — Calendar popup (floating)
 * Month grid + upcoming meetings. Meetings come from the
 * already-rendered .cal-event list (no extra fetch).
 * ============================================================ */
(function () {
  'use strict';

  const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const DOW = ['S','M','T','W','T','F','S'];
  const FALLBACK_EVENTS = { 3: 'Team Sync Meeting', 7: 'Project Alpha Review', 12: 'CyberSec Workshop' };
  let calDate = new Date();
  let selectedDay = new Date().getDate();

  function buildEvents(slot) {
    const ev = {};
    slot.querySelectorAll('.cal-event').forEach(el => {
      const dayEl = el.querySelector('.ev-date b');
      const titleEl = el.querySelector('.ev-main b');
      if (dayEl && titleEl) {
        const day = parseInt(dayEl.textContent.trim(), 10);
        if (!isNaN(day)) ev[day] = titleEl.textContent.trim();
      }
    });
    return Object.keys(ev).length ? ev : FALLBACK_EVENTS;
  }

  function renderCalendar(backdrop) {
    const grid = backdrop.querySelector('#calGrid');
    const label = backdrop.querySelector('#calLabel');
    if (!grid || !label) return;

    const y = calDate.getFullYear(), m = calDate.getMonth();
    label.textContent = MONTHS[m] + ' ' + y;

    const firstDay = new Date(y, m, 1).getDay();
    const daysInMonth = new Date(y, m + 1, 0).getDate();
    const prevDays = new Date(y, m, 0).getDate();
    const today = new Date();
    const isCurrentMonth = today.getFullYear() === y && today.getMonth() === m;
    const events = buildEvents(backdrop);

    let html = DOW.map(d => '<div class="cal-dow">' + d + '</div>').join('');
    for (let i = firstDay - 1; i >= 0; i--) html += '<div class="cal-day other">' + (prevDays - i) + '</div>';
    for (let d = 1; d <= daysInMonth; d++) {
      const cls = ['cal-day'];
      if (isCurrentMonth && d === today.getDate()) cls.push('today');
      if (d === selectedDay) cls.push('selected');
      if (events[d]) cls.push('has-event');
      html += '<div class="' + cls.join(' ') + '" data-day="' + d + '">' + d + '</div>';
    }
    grid.innerHTML = html;

    grid.querySelectorAll('.cal-day:not(.other)').forEach(day => {
      day.addEventListener('click', () => {
        selectedDay = parseInt(day.dataset.day, 10);
        renderCalendar(backdrop);
      });
    });
  }

  window.ZN.registerModal('calendar', {
    onOpen(backdrop) {
      renderCalendar(backdrop);
      const prev = backdrop.querySelector('#calPrev');
      const next = backdrop.querySelector('#calNext');
      if (prev && !prev.dataset.bound) {
        prev.dataset.bound = '1';
        prev.addEventListener('click', () => { calDate.setMonth(calDate.getMonth() - 1); renderCalendar(backdrop); });
      }
      if (next && !next.dataset.bound) {
        next.dataset.bound = '1';
        next.addEventListener('click', () => { calDate.setMonth(calDate.getMonth() + 1); renderCalendar(backdrop); });
      }
    }
  });
})();