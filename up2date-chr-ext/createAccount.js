function createAccount(json) {
    console.log(json)
    const Httpreq = new XMLHttpRequest();
    const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/auth/";
    Httpreq.open("POST", Httpurl, true);
    Httpreq.withCredentials = true;

    Httpreq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    Httpreq.onreadystatechange = function() {
        if (Httpreq.readyState == 4) {
            alert(Httpreq.responseText);
        }
    }

    Httpreq.send(json);
    alert("post sent!");
}