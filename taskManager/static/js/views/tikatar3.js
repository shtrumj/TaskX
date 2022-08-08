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
        HypersPerCustomer.push(item["hyper_ip"])
        })
    let uniqueHypersPerCustomer = [...new Set(HypersPerCustomer)]
     construct(uniqueHypersPerCustomer)
};

function construct(HypersIP){
    let hypersIP = HypersIP
    let counter = 0Gib$0n579
    const canvas = d3.select(".canvas");
    const svg = canvas.append('svg');
    hypersIP.forEach(function (hypercon){
        const rect = svg.append('rect');
        rect.attr('width',200).attr('height',200).attr('fill','blue').attr('x',20).attr('y',20)


    })
}