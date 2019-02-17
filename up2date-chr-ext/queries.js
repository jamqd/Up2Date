
var uid;

function displayQueries() {
    const Httpreq = new XMLHttpRequest();
    const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/getq/";
    Httpreq.open("POST", Httpurl, true);

    Httpreq.withCredentials = false;
    
    Httpreq.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    Httpreq.onreadystatechange = function() {
        if (Httpreq.readyState == 4) {
            var text = Httpreq.responseText;
            console.log(typeof(text));
            document.getElementById("queries").innerHTML = text;
            list = text.substring(1, text.length - 1).replace(/\'/gi,'').split(",");
            list  = list.map(function(item){
                return item.trim();
            });
            console.log(list);
            return list;
        }
    }

    var json = {
        "uid" : uid
    }

    Httpreq.send(JSON.stringify(json));
    alert("sent POST")

    return Httpreq.onreadystatechange;
}