/*
==========================================================
 ZeroNexus Animation Engine
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeRevealAnimations();
    initializeCardHover();
    initializeRippleEffect();
    initializeParallax();
    initializeFloatingCards();
    initializeGlowEffect();
    initializeScrollProgress();
    initializeTypingCursor();

});

/* ==========================================================
   Reveal Animation
========================================================== */

function initializeRevealAnimations() {

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("fade-up");

                observer.unobserve(entry.target);

            }

        });

    }, {

        threshold: .15

    });

    document.querySelectorAll(

        ".dashboard-card,.timeline-item,.stat-card"

    ).forEach(element => {

        observer.observe(element);

    });

}

/* ==========================================================
   Card Hover
========================================================== */

function initializeCardHover() {

    document.querySelectorAll(".dashboard-card")

    .forEach(card => {

        card.addEventListener("mousemove", e => {

            const rect = card.getBoundingClientRect();

            const x = e.clientX - rect.left;

            const y = e.clientY - rect.top;

            card.style.setProperty("--mouseX", x + "px");

            card.style.setProperty("--mouseY", y + "px");

        });

    });

}

/* ==========================================================
   Ripple Effect
========================================================== */

function initializeRippleEffect() {

    document.querySelectorAll(

        ".btn,.quick-action"

    ).forEach(button => {

        button.addEventListener("click", function(e) {

            const ripple = document.createElement("span");

            ripple.className = "ripple";

            const rect = this.getBoundingClientRect();

            ripple.style.left =

                e.clientX - rect.left + "px";

            ripple.style.top =

                e.clientY - rect.top + "px";

            this.appendChild(ripple);

            setTimeout(() => {

                ripple.remove();

            }, 700);

        });

    });

}

/* ==========================================================
   Floating Cards
========================================================== */

function initializeFloatingCards() {

    document.querySelectorAll(".float")

    .forEach((card,index)=>{

        card.style.animationDelay =

            (index*.2)+"s";

    });

}

/* ==========================================================
   Glow Effect
========================================================== */

function initializeGlowEffect(){

    document.querySelectorAll(".glow")

    .forEach(card=>{

        card.addEventListener("mouseenter",()=>{

            card.style.boxShadow=

            "0 0 35px rgba(0,191,255,.35)";

        });

        card.addEventListener("mouseleave",()=>{

            card.style.boxShadow="";

        });

    });

}

/* ==========================================================
   Scroll Progress
========================================================== */

function initializeScrollProgress(){

    const bar=document.querySelector("#scrollProgress");

    if(!bar)return;

    window.addEventListener("scroll",()=>{

        const height=

            document.documentElement.scrollHeight-

            window.innerHeight;

        const percent=

            (window.scrollY/height)*100;

        bar.style.width=percent+"%";

    });

}

/* ==========================================================
   Typing Cursor
========================================================== */

function initializeTypingCursor(){

    document

    .querySelectorAll(".cursor")

    .forEach(cursor=>{

        setInterval(()=>{

            cursor.style.opacity=

            cursor.style.opacity==="0"

            ?"1":"0";

        },550);

    });

}

/* ==========================================================
   Dashboard Entrance
========================================================== */

window.addEventListener("load",()=>{

    document

    .querySelectorAll(".dashboard-card")

    .forEach((card,index)=>{

        card.style.opacity="0";

        card.style.transform="translateY(30px)";

        setTimeout(()=>{

            card.style.transition=

            "all .5s ease";

            card.style.opacity="1";

            card.style.transform=

            "translateY(0)";

        },index*120);

    });

});

/* ==========================================================
   Counter Observer
========================================================== */

const counterObserver=

new IntersectionObserver(entries=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            const el=entry.target;

            const target=

            parseInt(el.dataset.target||0);

            let value=0;

            const timer=setInterval(()=>{

                value+=Math.ceil(target/50);

                if(value>=target){

                    value=target;

                    clearInterval(timer);

                }

                el.innerHTML=value;

            },20);

            counterObserver.unobserve(el);

        }

    });

});

document

.querySelectorAll(".animated-counter")

.forEach(counter=>{

    counterObserver.observe(counter);

});

/* ==========================================================
   Theme Transition
========================================================== */

function smoothThemeTransition(){

    document.body.style.transition=

    "background .4s,color .4s";

}

smoothThemeTransition();