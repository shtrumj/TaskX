// // window.addEventListener('DOMContentLoaded', (event) => {
// //     const select = document.getElementById("customer");
// //     console.log(select.value)});
// window.addEventListener('DOMContentLoaded', (event) => {
//     clientname= document.getElementById("name");
//     clientcity= document.getElementById("city");
//     clientadd = document.getElementById("address");
//     clientind= document.getElementById("internalDomain");
//     clientexd= document.getElementById("externalDomain");
//     clientowadd= document.getElementById("owaadd");
//     submit = document.getElementById("submit");
//     clientname.value += custname
//     clientcity.value += custcity
//     clientadd.value += custadd
//     clientind.value += custindomain
//     clientexd.value += custexdomain
//     clientowadd.value += custowaadd
//     submit.value = 'ערוך לקוח'
// });
function myfunc(){
    clientname= document.getElementById("name");
    clientcity= document.getElementById("city");
    clientadd = document.getElementById("address");
    clientind= document.getElementById("internalDomain");
    clientexd= document.getElementById("externalDomain");
    clientowadd= document.getElementById("owaadd");
    clientname.value += custname
    clientcity.value += custcity
    clientadd.value += custadd
    clientind.value += custindomain
    clientexd.value += custexdomain
    clientowadd.value += custowaadd
    console.log(custcity);
}