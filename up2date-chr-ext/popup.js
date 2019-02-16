function queryHighlight() {
    chrome.tabs.executeScript( {
        code: "window.getSelection().toString();"
    }, function(selection) {
        //document.getElementById("output").innerHTML = selection[0];
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/q/";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        Httpreq.onreadystatechange = function() {
            if (Httpreq.readyState == 4) {
                alert(Httpreq.responseText);
            }
        }

        Httpreq.send(selection[0]);
        alert("post sent!");
    });
}

function queryTitle() {
    chrome.tabs.getSelected(null, function(tab) {
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/q/";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        var tab_title = tab.title;
        Httpreq.onreadystatechange = function() {
            if (Httpreq.readyState == 4) {
                alert(Httpreq.responseText);
            }
        }

        Httpreq.send(tab_title);
        alert("post sent!");
    });
}

window.onload=function() {
    document.getElementById('query-highlight').addEventListener('click', queryHighlight);
    document.getElementById('query-title').addEventListener('click', queryTitle);
}

