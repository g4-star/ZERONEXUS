/*
==================================================
Notifications
==================================================
*/

function toast(message){

    const toast=document.createElement("div");

    toast.className="toast-message";

    toast.innerHTML=`

        🔔 ${message}

    `;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.remove();

    },4000);

}

/* Demo */

setTimeout(()=>{

    toast("Welcome back to ZeroNexus!");

},1500);