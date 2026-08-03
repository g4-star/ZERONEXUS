/* ============================================================
 * ZeroNexus — Profile popup polish
 * Completion bar + ring animations whenever the popup opens.
 * ============================================================ */
(function () {
  'use strict';

  function animateCompletions(root) {
    root.querySelectorAll('.comp-fill[data-w]').forEach(bar => {
      bar.style.width = bar.dataset.w + '%';
    });
  }

  window.ZN.registerModal('profile', {
    onOpen(backdrop) {
      // Small delay so the pop-in animation is visible first
      requestAnimationFrame(() => setTimeout(() => animateCompletions(backdrop), 60));
    }
  });
})();