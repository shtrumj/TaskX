function create_div() {
    const New_div = document.createElement('div');
    New_div.style.width = "100px";
    New_div.style.height = "100px";
    New_div.style.background = "red";
    New_div.innerHTML = "Test";
    New_div.style.display = "block";
    document.body.appendChild('new_div')
}


window.addEventListener('load', (event) => {
    let email = document.getElementById('clientEmailAddress');
    email.addEventListener('change', create_div);
});