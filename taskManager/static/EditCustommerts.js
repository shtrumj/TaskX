// window.addEventListener('DOMContentLoaded', (event) => {
//     const select = document.getElementById("customer");
//     console.log(select.value)});

function myfunc(){
    let select = document.getElementById("customer");
    var value = select.options[select.selectedIndex].values;
    form = document.getElementById("clientForm");
    form.appendChild(select);
    form.submit();
}