function addElement() {
    const element = document.getElementById("lista");
    let li = document.createElement("li");
    li.innerHTML = "Novo Item";

    element.append(li);
}

addElement()