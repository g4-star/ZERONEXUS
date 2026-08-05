/*
==================================================
ZeroNexus Chat
==================================================
*/

document.addEventListener("DOMContentLoaded",()=>{

    setupChat();

});

/* ===================================== */

function setupChat(){

    const input=document.querySelector("#chatInput");

    const send=document.querySelector("#sendMessage");

    const container=document.querySelector(".chat-messages");

    if(!input||!send||!container){

        return;

    }

    send.onclick=()=>{

        const text=input.value.trim();

        if(!text)return;

        appendMessage("You",text,true);

        input.value="";

    };

    input.addEventListener("keypress",(e)=>{

        if(e.key==="Enter"){

            send.click();

        }

    });

}

/* ===================================== */

function appendMessage(user,message,own=false){

    const container=document.querySelector(".chat-messages");

    const wrapper=document.createElement("div");

    wrapper.className=

        own?

        "message text-end mb-3":

        "message mb-3";

    wrapper.innerHTML=`

        <strong>${user}</strong>

        <div class="chat-bubble ${own?'own-message':''}">

            ${message}

        </div>

    `;

    container.appendChild(wrapper);

    container.scrollTop=container.scrollHeight;

}