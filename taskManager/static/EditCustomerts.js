"use strict";
function myfunc(){
    let cselect = document.getElementById("mycustomer");
    let mySelect =cselect.value;
    let cvalue1 = cselect.options[cselect.selectedIndex].text;
    let clientid= document.getElementById("cid");
    let clientname= document.getElementById("name");
    let clientcity= document.getElementById("city");
    let clientadd = document.getElementById("address");
    let clientind= document.getElementById("internalDomain");
    let clientexd= document.getElementById("externalDomain");
    let clientowadd= document.getElementById("owaadd");
    cust_fetch(mySelect);


};

async function cust_fetch(mySelect) {
    let sel = mySelect
    const response = await fetch(
        'http://' + window.location.host + '/it',
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
            show(data, sel);
        });
}
function show(data, sel){
    let mySelect = sel;
    let cselect = document.getElementById("mycustomer");
    let cvalue1 = cselect.options[cselect.selectedIndex].text;
    let mydata =data.data;
    console.log("your selection is " ,mySelect)
    var newArray = mydata.filter(function(id){
        return id.id == mySelect;
    });
    console.log( newArray)
        let clientname= document.getElementById("name");
        let clientcity= document.getElementById("city");
        let clientadd = document.getElementById("address")
        let clientind= document.getElementById("internalDomain");
        let clientexd= document.getElementById("externalDomain");
        let clientowadd= document.getElementById("owaadd");

        clientname.value = newArray[0].name;
        clientcity.value = newArray[0].city;
        clientadd.value = newArray[0].address;
        clientind.value = newArray[0].internalDomain;
        clientexd.value = newArray[0].externalDomain;
        clientowadd.value = newArray[0].owaAdd;
};