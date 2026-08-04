/* ============================================================
 * ZeroNexus Popup System
 * ============================================================ */

(function () {
    "use strict";

    window.ZeroNexus = window.ZeroNexus || {};

    const registry = {};
    let currentModal = null;

    function getModal(name) {
        return document.getElementById(`modal-${name}`);
    }

    function openModal(name) {

        if (!name) return;

        const backdrop = getModal(name);

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

        const closeButton = backdrop.querySelector("[data-close]");

        if (closeButton) {

            closeButton.focus();

        }

        if (registry[name] && typeof registry[name].onOpen === "function") {

            registry[name].onOpen(backdrop);

        }

    }

    function closeModal(name) {

        if (!name) return;

        const backdrop = getModal(name);

        if (!backdrop) return;

        backdrop.hidden = true;

        delete backdrop.dataset.open;

        if (registry[name] && typeof registry[name].onClose === "function") {

            registry[name].onClose(backdrop);

        }

        if (currentModal === name) {

            currentModal = null;

        }

        document.body.classList.remove("no-scroll");

    }

    function registerModal(name, hooks = {}) {

        registry[name] = hooks;

    }

    document.addEventListener("click", function (event) {

        /* -----------------------------
           OPEN MODAL
        ------------------------------ */

        const opener = event.target.closest("[data-modal]");

        if (opener) {

            event.preventDefault();

            openModal(opener.dataset.modal);

            return;

        }

        /* -----------------------------
           CLOSE BUTTON
        ------------------------------ */

        const closer = event.target.closest("[data-close]");

        if (closer) {

            event.preventDefault();

            const modal = closer.closest(".modal-backdrop");

            if (modal) {

                const name = modal.id.replace("modal-", "");

                closeModal(name);

            }

            return;

        }

        /* -----------------------------
           CLICK OUTSIDE MODAL
        ------------------------------ */

        const backdrop = event.target.closest(".modal-backdrop");

        if (backdrop && event.target === backdrop) {

            const name = backdrop.id.replace("modal-", "");

            closeModal(name);

        }

    });

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape" && currentModal) {

            closeModal(currentModal);

        }

    });

    window.ZeroNexus.openModal = openModal;
    window.ZeroNexus.closeModal = closeModal;
    window.ZeroNexus.registerModal = registerModal;

})();