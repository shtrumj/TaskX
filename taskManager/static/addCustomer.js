
function myfunc(){
    getCust()
    select = document.getElementById("mycustomer");
    console.log(select.value);
    clientid= document.getElementById("cid");
    clientname= document.getElementById("name");
    clientcity= document.getElementById("city");
    clientadd = document.getElementById("address");
    clientind= document.getElementById("internalDomain");
    clientexd= document.getElementById("externalDomain");
    clientowadd= document.getElementById("owaadd");
    clientname.value += custname
    clientid.value += custid
    clientcity.value += custcity
    clientadd.value += custadd
    clientind.value += custindomain
    clientexd.value += custexdomain
    clientowadd.value += custowaadd
    console.log(custcity);
}
async function getCust(){
     const api_url = 'http://127.0.0.1:8765/it'
     const response = await fetch(api_url, {});
     const data = await response.json();
     clientid.value = data[select.value -1].id;
     clientid.style.visibility = "hidden";
     clientname.value = data[select.value -1].name;
     clientcity.value = data[select.value -1].city;
     clientadd.value = data[select.value -1].address;
     clientind.value = data[select.value -1].internalDomain;
     clientexd.value = data[select.value -1].externalDomain;
     clientowadd.value = data[select.value -1].owaAdd;
}