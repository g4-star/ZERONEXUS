/*
==================================================
Animated Statistics
==================================================
*/

document.addEventListener("DOMContentLoaded",()=>{

    animateCounters();

});

/* ===================================== */

function animateCounters(){

    document.querySelectorAll(".counter")

    .forEach(counter=>{

        const target=parseInt(counter.dataset.target);

        let current=0;

        const speed=25;

        const update=()=>{

            current+=Math.ceil(target/50);

            if(current>=target){

                current=target;

            }

            counter.innerText=current;

            if(current<target){

                setTimeout(update,speed);

            }

        };

        update();

    });

}

/* ===================================== */

document

.querySelectorAll(".progress-circle")

.forEach(circle=>{

    const value=circle.dataset.progress;

    const circumference=377;

    const offset=

        circumference-

        (value/100)*circumference;

    circle.style.strokeDashoffset=offset;

});