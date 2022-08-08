function GetSelection() {
    myCustomerSelection = document.getElementById('mycustomer').value
    servers2customers(myCustomerSelection)
}

async function servers2customers(customerSelection){
    const customer = customerSelection
    HypersPerCustomer =[]
    ServersURL = 'http://' + window.location.host + '/ser/' + customer;
    const ServersResponse = await fetch(
            ServersURL,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                mode: 'cors',
                cache: 'default'
            }
        )
    const ServersPerCustomerData = await ServersResponse.json();
    ServersPerCustomerData['data'].forEach(function (item){
        HypersPerCustomer.push(item["hyper_id"])
        })
    let uniqueHypersPerCustomer = [...new Set(HypersPerCustomer)]
    console.log(uniqueHypersPerCustomer)

};