
var uid = "-LYshCmequUOw-w7wAgG";

function getQueries() {
    const Httpreq = new XMLHttpRequest();
    const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/getq/";
    Httpreq.open("POST", Httpurl, true);

    Httpreq.withCredentials = false;
    
    Httpreq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    Httpreq.onreadystatechange = function() {
        if (Httpreq.readyState == 4) {
            console.log(Httpreq.responseText);
            return Httpreq.responseText;
        }
    }

    var json = {
        "uid" : uid
    }

    Httpreq.send(JSON.stringify(json));
    alert("sent POST")
}

function displayQueries(){
    var qList = JSON.parse(getQueries());
    console.log(qList)
    document.getElementById("queries").innerHTML = qList;
}