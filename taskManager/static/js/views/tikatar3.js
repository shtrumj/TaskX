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
    let counter = 0;
    const canvas = d3.select(".canvas");
    const svg = canvas.append('svg')
        svg.attr("width","100%").attr("height","1000")
    hypersIP.forEach(function (hypercon) {
        const rect = svg.append('rect');
        rect.attr('width', 200).attr('height', 200).attr('fill', 'green').attr('x', 0 + counter).attr('y', 20).attr("rx","20").attr("preserveAspectRatio","xMaxYMin meet")
        const text = svg.append('text');
        text.attr('fill', 'black').attr('x', 0).attr('y', 0).text(hypercon).attr('font-size', "55")
        counter += 400
        console.log(counter)
    })

}