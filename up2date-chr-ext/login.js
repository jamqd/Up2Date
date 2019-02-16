function login(json) {
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

function myFunction() {
    console.log(document.getElementById("email").value);
    console.log(document.getElementById("password").value);
    json = {
        "email": document.getElementById("email").value,
        "password" : document.getElementById("password").value
    }
    login(json)
  }

window.onload=function() {
    document.getElementById('obutton').addEventListener('click', myFunction);
}