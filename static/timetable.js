const tabs = document.getElementsByClassName("tab")
const add = document.getElementById("add_task")
const remove = document.getElementById("remove_task")

const add_content = document.getElementById("add_task_content")
const remove_content = document.getElementById("remove_task_content")

function hide_tabs(){
    for (i = 0; i < tabs.length; i++) {
        tabs[i].style.display = "none";
    }
}

add.addEventListener("click", function (){
    hide_tabs()
    add_content.style.display = "block";
})
remove.addEventListener("click", function(){
    hide_tabs()
    remove_content.style.display = "block";
})

hide_tabs()