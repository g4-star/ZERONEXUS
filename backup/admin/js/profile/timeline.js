/*
==================================================
Timeline
==================================================
*/

const items=

document.querySelectorAll(".timeline-item");

const observer=

new IntersectionObserver(entries=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("fade-up");

        }

    });

});

items.forEach(item=>observer.observe(item));