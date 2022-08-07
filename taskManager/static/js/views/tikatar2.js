function selectB() {
    myCustomerSelection = document.getElementById('mycustomer').value
    fetchHypers(myCustomerSelection)
}

async function fetchHypers(myCustomerSelection){
    selectM = myCustomerSelection
    hyperesURL = 'http://' + window.location.host + '/hypers';
    const myHypers = await fetch(
        hyperesURL,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            cache: 'default'
        }
    )
    const hypersData = await myHypers.json();
    const mySelectedHypes = await  hypersData['data'].filter(({custid}) => custid == selectM);
    mySelectedHypes.forEach(function (test){
    const hypips = (test['ip_address'])
    construct(hypips)
    });

};

function construct(hips) {
    console.log(hips)
    const w = 500;
    const h = 200;
    const svg = d3.select('body')
        .append("svg")
        .attr('width', w)
        .attr('height', h)
        .attr('class' , "GoodClass")
}