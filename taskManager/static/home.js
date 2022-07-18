
function hideSubmit(){
   document.getElementById('submit').style.display='none';
}

// document.addEventListener("DOMContentLoaded", hideSubmit);

const checkBox=document.getElementsByName('task-checkbox');
checkBox.addEventListener('click', function(){
    document.getElementById('submit').style.display='block';
});


// const submit = document.querySelectorAll('input[name="task-checkbox"]:checked');