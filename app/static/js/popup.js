/* ============================================================
 * ZeroNexus — reusable popup system (Slack-style floating windows)
 * openModal("chat") / closeModal()
 * Lazy: popup content lives in <template id="tpl-*"> and is cloned
 * into the modal slot only on first open, then cached & reused.
 * ============================================================ */
(function () {
  'use strict';

  const registry = {};            // feature hooks: { onOpen, onClose }
  const opened = { current: null };

  function registerModal(name, hooks) {
    registry[name] = hooks || {};
  }

  function openModal(name) {
    const backdrop = document.getElementById('modal-' + name);
    if (!backdrop) return;

    const slot = backdrop.querySelector('[data-slot]');
    if (slot && !slot.dataset.loaded) {
      const tpl = document.getElementById('tpl-' + name);
      if (tpl && tpl.content) {
        slot.appendChild(tpl.content.cloneNode(true));
      }
      slot.dataset.loaded = '1';
    }

    // Close any previously open modal first (only one at a time)
    if (opened.current && opened.current !== name) closeModal(opened.current, { silent: true });

    backdrop.hidden = false;
    document.body.classList.add('no-scroll');
    opened.current = name;
    backdrop.dataset.open = '1';

    const closeBtn = backdrop.querySelector('[data-close]');
    if (closeBtn) closeBtn.focus();

    if (registry[name] && typeof registry[name].onOpen === 'function') {
      registry[name].onOpen(backdrop);
    }
  }

  function closeModal(name, opts) {
    const backdrop = document.getElementById('modal-' + name);
    if (!backdrop || backdrop.hidden) return;

    backdrop.hidden = true;
    delete backdrop.dataset.open;

    if (opts && opts.silent) return;
    if (opened.current === name) {
      opened.current = null;
      if (!document.querySelector('.modal-backdrop[data-open]')) {
        document.body.classList.remove('no-scroll');
      }
    }

    if (registry[name] && typeof registry[name].onClose === 'function') {
      registry[name].onClose(backdrop);
    }
  }

  /* ---- Global delegation: any [data-modal] opens, [data-close] closes ---- */
  document.addEventListener('click', function (e) {
    const opener = e.target.closest('[data-modal]');
    if (opener) {
      e.preventDefault();
      openModal(opener.dataset.modal);
      return;
    }
    const closer = e.target.closest('[data-close]');
    if (closer) {
      e.preventDefault();
      const root = closer.closest('.modal-backdrop');
      closeModal(root ? root.dataset.modalRoot : opened.current);
      return;
    }
    // Click on backdrop (not the shell) closes
    if (e.target.classList && e.target.classList.contains('modal-backdrop')) {
      closeModal(e.target.dataset.modalRoot);
    }
  });

  // Escape key closes
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && opened.current) closeModal(opened.current);
  });

  // Expose to other feature scripts
  window.ZN = { openModal, closeModal, registerModal };
})();