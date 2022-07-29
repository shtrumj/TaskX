function atar() {
    let cselect = document.getElementById("mycustomer");
    let mySelect =cselect.value;
    console.log(mySelect)
    hyperfetch()
}


async function hyperfetch(){
        const response = await fetch(
        'http://' + window.location.host + '/hypers',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            cache : 'default'}
    );
        const Myhypers = await response.json();
        console.log(Myhypers.data)
}
function getSelection(){

}
