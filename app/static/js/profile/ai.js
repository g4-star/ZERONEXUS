/*
==================================================
ZeroNexus AI
==================================================
*/

const aiInput=document.querySelector("#aiPrompt");

const aiSend=document.querySelector("#askAI");

const terminal=document.querySelector(".terminal-body");

if(aiSend){

    aiSend.onclick=()=>{

        const prompt=aiInput.value.trim();

        if(!prompt)return;

        terminal.innerHTML+=`

> ${prompt}

AI is thinking...

`;

        aiInput.value="";

        setTimeout(()=>{

            terminal.innerHTML+=`

✔ Response generated.

`;

            terminal.scrollTop=

            terminal.scrollHeight;

        },1200);

    };

}