const focus_tab = document.getElementById("focus")
const toggle_focus = document.getElementById("toggle_focus")
const page = document.getElementsByClassName("hide")

const term = document.getElementById("term");
const definition = document.getElementById("definition");

const reveal = document.getElementById("Reveal");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let cardIdx = 0;
let cardData = load();

const revision_set = document.getElementById("revision_set");
let active_set = revision_set.value;

const set_to_add_card = document.getElementById("set_to_add_card");

async function load() {
    const response = await fetch("/static/revision.JSON");
    cardData = await response.json();
    return cardData;
}

function display(){
    let dataOptions = Object.entries(cardData[active_set]);
    try {
        term.innerHTML = dataOptions[cardIdx][0];
    }
    catch(err){
        term.innerHTML = "Add Some Cards!";
    }
    definition.style.display = "none";
}

function showAns(){
    definition.style.display = "block";
    let dataOptions = Object.entries(cardData[active_set]);
    try {
        term.innerHTML = dataOptions[cardIdx][0];
        definition.innerHTML = dataOptions[cardIdx][1];
    }
    catch(err){
        term.innerHTML = "Add Some Cards!";
        definition.style.display = "none";
    }
}

revision_set.addEventListener("click", function(){
    active_set = revision_set.value;
    set_to_add_card.value = active_set;
    display();
})

reveal.addEventListener("click", function(){
    showAns();
})

prevBtn.addEventListener("click", function(){
    if (cardIdx < 1){
        cardIdx += 1;
    }
    cardIdx -= 1;
    display();
})

nextBtn.addEventListener("click", function(){
    if (cardIdx >= Object.keys(cardData[active_set]).length - 1){
        cardIdx -= 1;
    }
    cardIdx += 1;
    display();
})

toggle_focus.addEventListener("click", function(){
    if (toggle_focus.innerHTML == "focus"){
        toggle_focus.innerHTML = "leave focus"
        for (let i = 0; i < page.length; i++) {
            page[i].style.display = "none";
        }
        focus_tab.display = "block";
    }
    else {
        toggle_focus.innerHTML = "focus"
        for (let i = 0; i < page.length; i++) {
            page[i].style.display = "block";
        }
    }
})