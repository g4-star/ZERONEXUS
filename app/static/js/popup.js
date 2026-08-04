/* ============================================================
 * ZeroNexus Popup System
 * Safe Version
 * ============================================================ */

(function () {
    "use strict";

    // Create namespace if it doesn't exist
    window.ZeroNexus = window.ZeroNexus || {};

    const registry = {};
    let currentModal = null;

    function openModal(name) {

        if (!name) return;

        const backdrop = document.getElementById(`modal-${name}`);

        if (!backdrop) {
            console.warn(`Modal "${name}" not found.`);
            return;
        }

        const slot = backdrop.querySelector("[data-slot]");

        if (slot && !slot.dataset.loaded) {

            const template = document.getElementById(`tpl-${name}`);

            if (template && template.content) {
                slot.appendChild(template.content.cloneNode(true));
            }

            slot.dataset.loaded = "true";
        }

        if (currentModal && currentModal !== name) {
            closeModal(currentModal);
        }

        backdrop.hidden = false;
        backdrop.dataset.open = "true";

        document.body.classList.add("no-scroll");

        currentModal = name;

        const closeBtn = backdrop.querySelector("[data-close]");

        if (closeBtn) {
            closeBtn.focus();
        }

        if (registry[name]?.onOpen) {
            registry[name].onOpen(backdrop);
        }

    }

    function closeModal(name) {

        const backdrop = document.getElementById(`modal-${name}`);

        if (!backdrop) return;

        backdrop.hidden = true;

        delete backdrop.dataset.open;

        if (registry[name]?.onClose) {
            registry[name].onClose(backdrop);
        }

        currentModal = null;

        document.body.classList.remove("no-scroll");

    }

    function registerModal(name, hooks = {}) {

        registry[name] = hooks;

    }

    document.addEventListener("click", function (e) {

        const opener = e.target.closest("[data-modal]");

        if (opener) {

            e.preventDefault();

            openModal(opener.dataset.modal);

            return;

        }

        const closer = e.target.closest("[data-close]");

        if (closer) {

            e.preventDefault();

            const modal = closer.closest(".modal-backdrop");

            if (modal) {

                closeModal(modal.dataset.modalRoot);

            }

            return;

        }

        if (e.target.classList.contains("modal-backdrop")) {

            closeModal(e.target.dataset.modalRoot);

        }

    });

    document.addEventListener("keydown", function (e) {

        if (e.key === "Escape" && currentModal) {

            closeModal(currentModal);

        }

    });

    // Don't overwrite the namespace
    window.ZeroNexus.openModal = openModal;
    window.ZeroNexus.closeModal = closeModal;
    window.ZeroNexus.registerModal = registerModal;

})();