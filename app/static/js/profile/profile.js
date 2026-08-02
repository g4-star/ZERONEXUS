/*
==========================================================
ZeroNexus Dashboard
Main Initializer
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    console.log("ZeroNexus Dashboard Loaded");

    initializeCards();

    initializeButtons();

    initializeAnimations();

});

/* ============================================= */

function initializeCards(){

    document
        .querySelectorAll(".dashboard-card")
        .forEach(card=>{

            card.addEventListener("mouseenter",()=>{

                card.style.transform="translateY(-8px)";

            });

            card.addEventListener("mouseleave",()=>{

                card.style.transform="translateY(0px)";

            });

        });

}

/* ============================================= */

function initializeButtons(){

    document
        .querySelectorAll(".btn")
        .forEach(button=>{

            button.addEventListener("mousedown",()=>{

                button.style.transform="scale(.96)";

            });

            button.addEventListener("mouseup",()=>{

                button.style.transform="";

            });

        });

}

/* ============================================= */

function initializeAnimations(){

    const observer=new IntersectionObserver(entries=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("fade-up");

            }

        });

    });

    document
        .querySelectorAll(".dashboard-card")
        .forEach(card=>{

            observer.observe(card);

        });

}