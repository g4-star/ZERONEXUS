/*
==================================================
Dashboard Controller
==================================================
*/

document.addEventListener("DOMContentLoaded",()=>{

    console.log("Dashboard Ready");

    refreshClock();

    setInterval(refreshClock,1000);

});

/* ===================================== */

function refreshClock(){

    const clock=document.querySelector("#dashboardClock");

    if(!clock)return;

    const now=new Date();

    clock.innerHTML=

        now.toLocaleTimeString();

}