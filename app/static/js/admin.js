/* ============================================================
   ZeroNexus Admin — frontend interactions
   Sidebar drawer, notifications, global search, calendar,
   staggered animations, flash auto-dismiss
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. Mobile sidebar drawer ---------- */
  const sidebar = document.getElementById('adminSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  const navToggle = document.getElementById('navToggle');

  if (sidebar && backdrop && navToggle) {
    const openSidebar = () => {
      sidebar.classList.add('open');
      backdrop.classList.add('show');
      document.body.style.overflow = 'hidden';
    };

    const closeSidebar = () => {
      sidebar.classList.remove('open');
      backdrop.classList.remove('show');
      document.body.style.overflow = '';
    };

    navToggle.addEventListener('click', () => {
      if (sidebar.classList.contains('open')) closeSidebar();
      else openSidebar();
    });

    backdrop.addEventListener('click', closeSidebar);

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSidebar();
    });
  }

  /* ---------- 2. Notification dropdown ---------- */
  const notifWrap = document.querySelector('.notif-wrap');
  const notifToggle = document.getElementById('notifToggle');

  if (notifWrap && notifToggle) {
    notifToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      notifWrap.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (!notifWrap.contains(e.target)) notifWrap.classList.remove('open');
    });
  }

  /* ---------- 3. Global table search (live filter) ---------- */
  const searchInput = document.getElementById('globalSearch');

  if (searchInput) {
    const tables = document.querySelectorAll('table[data-searchable]');

    const filterRows = () => {
      const q = searchInput.value.trim().toLowerCase();

      tables.forEach((table) => {
        const rows = table.querySelectorAll('tbody tr');
        let visible = 0;

        rows.forEach((row) => {
          const match = row.textContent.toLowerCase().includes(q);
          row.style.display = match ? '' : 'none';
          if (match) visible += 1;
        });

        let empty = table.parentElement.querySelector('.search-empty');

        if (q && visible === 0) {
          if (!empty) {
            empty = document.createElement('div');
            empty.className = 'search-empty';
            empty.textContent = 'No results found.';
            table.insertAdjacentElement('afterend', empty);
          }
          empty.style.display = 'block';
        } else if (empty) {
          empty.style.display = 'none';
        }
      });
    };

    searchInput.addEventListener('input', filterRows);
  }

  /* ---------- 4. Calendar widget ---------- */
  const calendar = document.getElementById('calendarWidget');
  const monthLabel = document.getElementById('calendarMonthLabel');
  const activityDate = document.getElementById('activityDate');

  // Live date labels (real current date, no hardcoded data)
  if (activityDate) {
    activityDate.textContent = new Date().toLocaleDateString(undefined, {
      weekday: 'long', month: 'long', day: 'numeric'
    });
  }

  if (calendar) {
    const now = new Date();
    const today = { y: now.getFullYear(), m: now.getMonth(), d: now.getDate() };
    let view = { y: today.y, m: today.m };

    const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
    const DOW = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

    // Optional event dates from data-events (JSON array of "YYYY-MM-DD")
    let events = [];
    try {
      events = JSON.parse(calendar.dataset.events || '[]');
    } catch (err) {
      events = [];
    }

    const pad = (n) => String(n).padStart(2, '0');
    const dateKey = (y, m, d) => `${y}-${pad(m + 1)}-${pad(d)}`;

    function render() {
      const firstOffset = (new Date(view.y, view.m, 1).getDay() + 6) % 7; // Monday-first
      const daysInMonth = new Date(view.y, view.m + 1, 0).getDate();
      const daysPrev = new Date(view.y, view.m, 0).getDate();
      const total = Math.ceil((firstOffset + daysInMonth) / 7) * 7;

      monthLabel.textContent = `${MONTHS[view.m]} ${view.y}`;

      let html = '<div class="cal-grid">';
      DOW.forEach((d) => { html += `<div class="cal-dow">${d}</div>`; });

      for (let i = 0; i < total; i++) {
        const dayNum = i - firstOffset + 1;
        let cls = 'cal-day';
        let label;

        if (dayNum < 1) {
          label = daysPrev + dayNum;
          cls += ' other';
        } else if (dayNum > daysInMonth) {
          label = dayNum - daysInMonth;
          cls += ' other';
        } else {
          label = dayNum;
          if (dayNum === today.d && view.m === today.m && view.y === today.y) cls += ' today';
          if (events.includes(dateKey(view.y, view.m, dayNum))) cls += ' has-event';
        }

        html += `<div class="${cls}">${label}</div>`;
      }

      html += '</div>';
      calendar.innerHTML = html;
    }

    const prevBtn = document.querySelector('.cal-prev');
    const nextBtn = document.querySelector('.cal-next');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        view.m -= 1;
        if (view.m < 0) { view.m = 11; view.y -= 1; }
        render();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        view.m += 1;
        if (view.m > 11) { view.m = 0; view.y += 1; }
        render();
      });
    }

    render();
  }

  /* ---------- 5. Staggered entrance animations ---------- */
  document.querySelectorAll('.stagger').forEach((container, ci) => {
    Array.from(container.children).forEach((child, i) => {
      child.classList.add('anim-fade-up');
      child.style.animationDelay = `${ci * 0.08 + i * 0.07}s`;
    });
  });

  /* ---------- 6. Auto-dismiss flash alerts ---------- */
  document.querySelectorAll('.alert-dismissible').forEach((alertEl) => {
    setTimeout(() => {
      alertEl.classList.add('fade');
      setTimeout(() => alertEl.remove(), 300);
    }, 6000);
  });

  /* ---------- 7. Confirm dialogs (data-confirm) ---------- */
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[data-confirm]');
    if (link && link.getAttribute('data-confirm') &&
        !window.confirm(link.getAttribute('data-confirm'))) {
      e.preventDefault();
    }
  });

  document.addEventListener('submit', (e) => {
    const form = e.target.closest('form[data-confirm]');
    if (form && form.getAttribute('data-confirm') &&
        !window.confirm(form.getAttribute('data-confirm'))) {
      e.preventDefault();
    }
  });
})();

