/* ============================================================
 * ZeroNexus — Team Chat (floating popup)
 * Uses ONLY existing Flask routes:
 *   POST {{ send_chat }}    → team.send_chat
 *   GET  {{ messages_api }} → team.messages_api
 * No new routes, no page reloads.
 * ============================================================ */
(function () {
  'use strict';
  const CFG = window.ZN_CONFIG || {};
  let lastMsgId = 0;
  let pollTimer = null;
  let sending = false;

  function fmtTime(raw) {
    if (!raw) return '';
    const d = new Date(raw);
    if (isNaN(d)) return String(raw).slice(0, 16);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  async function loadMessages() {
    const box = document.getElementById('chatMessages');
    if (!box) return;
    try {
      const res = await fetch(CFG.messagesApiUrl, { headers: { 'X-Requested-With': 'fetch' } });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      const list = Array.isArray(data) ? data : (data.messages || []);
      if (!list.length) return;
      let newest = lastMsgId;
      list.forEach(m => {
        const id = Number(m.id);
        if (id > lastMsgId) {
          appendMessage(m);
          if (id > newest) newest = id;
        }
      });
      lastMsgId = Math.max(lastMsgId, newest);
    } catch (err) {
      console.warn('[chat] poll failed:', err);
    }
  }

  function appendMessage(m) {
    const box = document.getElementById('chatMessages');
    if (!box) return;
    const empty = box.querySelector('.chat-empty');
    if (empty) empty.remove();

    const author = (m.author && (m.author.username || m.author.full_name)) || m.username || 'Team';
    const isOwn = author === CFG.username;
    const initials = author.slice(0, 2).toUpperCase();

    const div = document.createElement('div');
    div.className = 'msg' + (isOwn ? ' own' : '');
    div.innerHTML =
      '<div class="msg-avatar">' + escapeHtml(initials) + '</div>' +
      '<div class="msg-bubble">' +
        '<div class="msg-meta"><span class="msg-author">' + escapeHtml(author) + '</span>' +
        '<span class="msg-time">' + escapeHtml(fmtTime(m.created_at)) + '</span></div>' +
        '<div class="msg-text">' + escapeHtml(m.message) + '</div>' +
      '</div>';

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  async function sendMessage(text) {
    if (sending || !text.trim()) return;
    sending = true;
    const input = document.getElementById('chatInput');
    const btn = document.querySelector('.chat-send');
    if (btn) btn.disabled = true;
    try {
      const res = await fetch(CFG.sendChatUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': CFG.csrf,
          'X-Requested-With': 'fetch'
        },
        body: JSON.stringify({ message: text.trim() })
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.error || 'HTTP ' + res.status);
      }
      if (input) input.value = '';
      if (window.ZN && ZN.showToast) ZN.showToast('Message sent to team 💬');
      await loadMessages();   // immediate refresh, poll continues behind
    } catch (err) {
      console.warn('[chat] send failed:', err);
      if (window.ZN && ZN.showToast) ZN.showToast('Message failed to send', true);
    } finally {
      sending = false;
      if (btn) btn.disabled = false;
      if (input) input.focus();
    }
  }

  function bindForm(backdrop) {
    const form = backdrop.querySelector('#chatForm');
    if (!form || form.dataset.bound) return;
    form.dataset.bound = '1';
    form.addEventListener('submit', e => {
      e.preventDefault();
      sendMessage(form.querySelector('#chatInput').value);
    });
  }

  window.ZN.registerModal('chat', {
    onOpen(backdrop) {
      bindForm(backdrop);
      loadMessages();
      clearInterval(pollTimer);
      pollTimer = setInterval(loadMessages, 3000);
    },
    onClose() {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  });
})();