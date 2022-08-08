function selectB() {
    myCustomerSelection = document.getElementById('mycustomer').value
    // const msvg = document.getElementsByClassName('canvas')
    //     msvg.firstChild.remove()

    fetchHypers(myCustomerSelection)
}

async function fetchHypers(myCustomerSelection){
    selectM = myCustomerSelection
    ipS = []
    HidS = []
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
    mySelectedHypes.forEach(function (filterHyper){
        ipS=[]
        HID=[]
        ipS.push(filterHyper['ip_address'])
        HID.push(filterHyper['id'])
    // console.log('ip is ' +ipS)
    // console.log('hid is ' +HID)
    construct(ipS, HID)
    });

};

function construct(ipS, HID) {
    ipS.forEach((ipS) => svgBuild(ipS, HID));


}

function svgBuild(Hyper_ip, HyperID){
    const canvas = d3.select(".canvas");
    const svg = canvas.append('svg');
        svg.attr('height','400')
        svg.attr('width', '600')
        svg.append('rect')
            .attr('width','200')
            .attr('height', '200')
            .attr('rx','20')
            .attr('class' , Hyper_ip)
            .attr('fill','blue')
        svg.append('text')
            .attr('x',150)
            .attr('y',20)
            .attr('fill', 'white')
            .style('font-weight','bold')
            .text(Hyper_ip)
        svg.append('text')
            .attr('x',150)
            .attr('y',40)
            .attr('fill', 'white')
            .style('font-weight','bold')
            .text(HyperID)
    async function FetchServer(HyperID) {
        ipS = []
        HidS = []
        ServersURL = 'http://' + window.location.host + '/servers';
        const myServers = await fetch(
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
        const ServersData = await myServers.json();
        const mySelectedServers = await ServersData.filter(({hyper_id}) => hyper_id == HyperID);
        mySelectedServers.forEach(function (myservers) {
            console.log(myservers)
        });
    }
    console.log('this is my Hyper ID ' + HyperID)




    // console.log(Hyper_ip)


}
