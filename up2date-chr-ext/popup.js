function queryHighlight() {
    chrome.tabs.executeScript( {
        code: "window.getSelection().toString();"
    }, function(selection) {
        document.getElementById("output").innerHTML = selection[0];
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        Httpreq.send(selection[0]);
    });
}

function queryTitle() {
    chrome.tabs.getCurrent(function(tab) {
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        Httpreq.send(tab.title);
    });
}

document.getElementById('query highlight').addEventListener('click', queryHighlight);
document.getElementById('query title').addEventListener('click', queryTitle);