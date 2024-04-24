function setBackgroundColor() {
    const element = document.getElementById("container");
    element.style.backgroundColor = "red";
}

function removeBackgroundColor() {
    const element = document.getElementById("container");
    element.style.backgroundColor = "inherit";
}

document.addEventListener("mouseover", setBackgroundColor);
document.addEventListener("mouseleave", removeBackgroundColor);