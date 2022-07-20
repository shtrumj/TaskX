"use strict";
function myfunc(){
    cust_fetch();
    let cselect = document.getElementById("mycustomer");
    let cvalue1 = cselect.options[cselect.selectedIndex].text;
    let clientid= document.getElementById("cid");
    let clientname= document.getElementById("name");
    let clientcity= document.getElementById("city");
    let clientadd = document.getElementById("address");
    let clientind= document.getElementById("internalDomain");
    let clientexd= document.getElementById("externalDomain");
    let clientowadd= document.getElementById("owaadd");
    // console.log(clientind)
    // console.log(cselect.value)
    // clientname.value += custname
    // clientid.value += custid
    // clientcity.value += custcity
    // clientadd.value += custadd
    // clientind.value += custindomain
    // clientexd.value += custexdomain
    // clientowadd.value += custowaadd

};

async function cust_fetch() {
    const response = await fetch(
        'http://15.21.16.12/it',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            cache : 'default'}
    ).then(function (resp) {
        return resp.json();
    })
        .then(function(data) {
            show(data);
        });
}
function show(data){
    let cselect = document.getElementById("mycustomer");
    let cvalue1 = cselect.options[cselect.selectedIndex].text;
    console.log(data);
}