function createAccount(json) {
    console.log(json)
    const Httpreq = new XMLHttpRequest();
    const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/auth/";
    Httpreq.open("POST", Httpurl, true);

    Httpreq.withCredentials = false;

    Httpreq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    Httpreq.onreadystatechange = function() {
        if (Httpreq.readyState == 4) {
            alert(Httpreq.responseText);
        }
    }

    Httpreq.send(JSON.stringify(json));
    alert("post sent!");
}
<<<<<<< HEAD
=======

function myFunction() {
    console.log(document.getElementById("name").value);
    console.log(document.getElementById("email").value);
    console.log(document.getElementById("password").value);
    json = {
        "name" : document.getElementById("name").value,
        "email": document.getElementById("email").value,
        "password" : document.getElementById("password").value
    }
    createAccount(json)
  }

window.onload=function() {
    document.getElementById('obutton').addEventListener('click', myFunction);
}
>>>>>>> 8c531f8a5c456d63c3fa485ca5f7134542a668cb
