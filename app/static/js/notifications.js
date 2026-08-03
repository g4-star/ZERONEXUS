/* ============================================================
 * ZeroNexus — Notification center (floating popup)
 * Client-side read-state (no backend route exists for it).
 * Badge syncs with unread count.
 * ============================================================ */
(function () {
  'use strict';

  function syncBadge(backdrop) {
    const badge = document.getElementById('notifBadge');
    if (!badge) return;
    const unread = backdrop ? backdrop.querySelectorAll('.notif-item.unread').length : 0;
    badge.textContent = unread;
    badge.classList.toggle('hidden', unread === 0);
    badge.classList.toggle('pulse', unread > 0);
  }

  function markRead(item) {
    item.classList.remove('unread');
    const root = item.closest('.modal-backdrop');
    syncBadge(root);
  }

  window.ZN.registerModal('notifications', {
    onOpen(backdrop) {
      syncBadge(backdrop);
      const list = backdrop.querySelector('#notifList');
      if (!list || list.dataset.bound) return;
      list.dataset.bound = '1';

      list.addEventListener('click', e => {
        const item = e.target.closest('.notif-item');
        if (item) markRead(item);
      });

      const clearBtn = backdrop.querySelector('#markAllRead');
      if (clearBtn) {
        clearBtn.addEventListener('click', () => {
          backdrop.querySelectorAll('.notif-item.unread').forEach(i => i.classList.remove('unread'));
          syncBadge(backdrop);
        });
      }
    }
  });
})();