const status = document.getElementById("status");


function hideReasonAndResolve(){
    resolve = document.getElementById("resolve");
    reason = document.getElementById("reason");
    resolveLabel = document.getElementById("resolveLabel");
    reasonLabel = document.getElementById("reasonLabel");
    whatHasBeenDone = document.getElementById("whatHasBeenDone")
    whatHasBeenDoneLabel = document.getElementById("whatHasBeenDoneLabel")
    // reason.style.display = "none";
    // reasonLabel.style.display = "none";
    resolveLabel.style.display= "none";
    resolve.style.display= "none";
    whatHasBeenDone.style.display="none";
    whatHasBeenDoneLabel.style.display="none";

}

function solve(){
    // resolve = document.getElementById("resolve");
    // resolveLabel = document.getElementById("resolveLabel")
    if (document.getElementById("status").value == "2") {
            reason.style.display = "none";
            reasonLabel.style.display = "none";
            whatHasBeenDone.style.display="none";
            whatHasBeenDoneLabel.style.display="none";
            resolve.style.display= "block";
            resolveLabel.style.display= "block";

    }
    else if (document.getElementById("status").value == "1") {
        reasonLabel.style.display= "block";
        reason.style.display= "block";
        resolve.style.display= "none";
        resolveLabel.style.display = "none";
        whatHasBeenDone.style.display="none";
        whatHasBeenDoneLabel.style.display="none";
    }
    else if (document.getElementById("status").value == "3") {
        resolve.style.display= "none";
        resolveLabel.style.display = "none";
        reason.style.display = "none";
        reasonLabel.style.display = "none";
        whatHasBeenDone.style.display="block";
        whatHasBeenDoneLabel.style.display="block";

    }
}

window.addEventListener('load', hideReasonAndResolve)
status.addEventListener('change',solve)
// function loadSts(){
//     status = document.getElementById("status").value;
//     resolve = document.getElementById("resolve");
//     if (document.getElementById("status").value != "בעיה נפתרה"){
//         resolve.style.display = "none";
//     }
// }
// stat = document.getElementById("status");
// stat.addEventListener('change', loadSts);
//

