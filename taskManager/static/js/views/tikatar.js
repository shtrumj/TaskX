function atar() {
    let cselect = document.getElementById("mycustomer");
    let mySelect =cselect.value;
    // console.log(mySelect)
    hyperfetch(mySelect)
}


async function hyperfetch(mySelect){
    let selection = mySelect
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
        console.log(Myhypers)
        console.log(selection)
}
function getSelection(){

}
