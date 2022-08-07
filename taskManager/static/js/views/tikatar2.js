function selectB() {
    myCustomerSelection = document.getElementById('mycustomer').value
    // const msvg = document.getElementsByClassName('canvas')
    //     msvg.firstChild.remove()

    fetchHypers(myCustomerSelection)
}

async function fetchHypers(myCustomerSelection){
    selectM = myCustomerSelection
    ipS = []
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
        ipS=[]
        ipS.push(test['ip_address'])
    // console.log(ipS)
    construct(ipS)
    });

};

function construct(ipS) {
    ipS.forEach((element) => svgBuild(element));

}

function svgBuild(ele){
    const canvas = d3.select(".canvas");
    const svg = canvas.append('svg');
        svg.attr('height','400')
        svg.attr('width', '600')
        svg.append('rect')
            .attr('width','200')
            .attr('height', '200')
            .attr('rx','20')
            .attr('class' , ele)
            .attr('fill','blue')
        svg.append('text')
            .attr('x',150)
            .attr('y',20)
            .attr('fill', 'white')
            .style('font-weight','bold')
            .text(ele)
    get_servers(ip)

async function get_servers(ip){
                hyperesURL = 'http://' + window.location.host + '/hypers';


}






    console.log(ele)


}
