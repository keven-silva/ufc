function addClassCss() {
    const listAttr = document.getElementsByClassName('item');
    
    for (const key of listAttr) {
        key.classList.add("destaque");
    }
}

addClassCss()