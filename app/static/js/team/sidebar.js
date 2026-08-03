document.querySelectorAll(".sidebar-link").forEach(link=>{

    link.addEventListener("click",()=>{

        document.querySelectorAll(".sidebar-link")
        .forEach(item=>item.classList.remove("active"));

        link.classList.add("active");

    });

});