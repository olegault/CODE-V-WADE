fetch('nav.html')
.then(res => res.text())
.then(text => {
    let oldelem = document.querySelector("script#navbar-place");
    let newelem = document.createElement("div");
    newelem.innerHTML = text;
    oldelem.parentNode.replaceChild(newelem,oldelem);
})