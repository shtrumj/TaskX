function myfunc(){
    let mycustomer = document.getElementById("mycustomer");
    let option = document.getElementById("options")
    let myselect= mycustomer.value;
    hyperfetch(myselect)

};

async function hyperfetch(myselect) {
    let sel = myselect
    const response = await fetch(
        'http://' + window.location.host + '/hypers',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            mode: 'cors',
            cache: 'default'}
    ).then(function (resp) {
        return resp.json();
    })
        .then(function(data) {
            show(data, sel);
        });
}

function show(data, sel) {
    let mySelect = sel;
    let mydata = data.data;
    // console.log("My Select is " + mySelect)
    // console.log("My Data is :" + mydata[0]["custid"])

    console.log("your selection is " ,mySelect)
    let newArray = mydata.filter(function (id) {
        return id.custid == mySelect;
    })
    let optionHTML = '';
    let ips = document.getElementById('ips')
    for (const obj of newArray) {
        optionHTML += '<option value="' + obj.ip_address + '">' + obj.ip_address + '</option>';
    }
    ips.innerHTML = optionHTML;
        // select.insertAdjacentHTML('beforeend', `
        // <option value ="${obj.ip_address}">${obj.ip_address}</option>
        // `)
        // option.append("<option>" + obj.ip_address + "</option")


        // $('hyperoptions').append($('<option>').val(obj.ip_address).text(obj.ip_address));
        // console.log(obj.ip_address)

    // for (let [key,value] of Object.entries(newArray)){
    //     console.log(`${value}`)
    // console.log(newArray);
    // for (let [key,value] of Object.entries(newArray)){
    //     if (key == 'ip_address'){
    //         console.log(`${key}: ${value}`);



}