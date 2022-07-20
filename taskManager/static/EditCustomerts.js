function myfunc(){
    cust_fetch();
    let cselect = document.getElementById("mycustomer");
    let cvalue= cselect.value;
    let cvalue1 = cselect.options[cselect.selectedIndex].text
    let clientid= document.getElementById("cid");
    let clientname= document.getElementById("name");
    let clientcity= document.getElementById("city");
    let clientadd = document.getElementById("address");
    let clientind= document.getElementById("internalDomain");
    let clientexd= document.getElementById("externalDomain");
    let clientowadd= document.getElementById("owaadd");
    clientname.value += custname
    clientid.value += custid
    clientcity.value += custcity
    clientadd.value += custadd
    clientind.value += custindomain
    clientexd.value += custexdomain
    clientowadd.value += custowaadd
    // console.log(select.value);
};
async function cust_fetch() {
    const response = await fetch(
        'http://127.0.0.1:8765/it',
        {
            method: 'GET'
        }
);
    const data = await resonse.json();
    consol.log(data)
}



