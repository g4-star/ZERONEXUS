/*
==================================================
Profile Modals
==================================================
*/

document

.querySelectorAll("[data-modal]")

.forEach(button=>{

    button.addEventListener("click",()=>{

        const id=button.dataset.modal;

        const modal=new bootstrap.Modal(

            document.getElementById(id)

        );

        modal.show();

    });

});

/* ===================================== */

document

.querySelectorAll(".modal")

.forEach(modal=>{

    modal.addEventListener("shown.bs.modal",()=>{

        modal

        .querySelector("input")?.focus();

    });

});