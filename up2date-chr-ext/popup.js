var uid;

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

function createFunction() {
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

  function login(json) {
    console.log(json)
    const Httpreq = new XMLHttpRequest();
    const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/login/";
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

function loginFunction() {
    console.log(document.getElementById("email").value);
    console.log(document.getElementById("password").value);
    json = {
        "email": document.getElementById("email").value,
        "password" : document.getElementById("password").value
    }
    login(json)
  }

function queryHighlight() {
    chrome.tabs.executeScript( {
        code: "window.getSelection().toString();"
    }, function(selection) {
        //document.getElementById("output").innerHTML = selection[0];
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/q/";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

        Httpreq.onreadystatechange = function() {
            if (Httpreq.readyState == 4) {
                alert(Httpreq.responseText);
            }
        }
        json = {
            "uid": uid,
            "query": selection[0]
        }

        Httpreq.send(json);
        alert("post sent!");
    });
}

function queryTitle() {
    chrome.tabs.getSelected(null, function(tab) {
        //user authentication goes here
        const Httpreq = new XMLHttpRequest();
        const Httpurl = "http://django-ev.2tuewqdzwb.us-west-1.elasticbeanstalk.com/q/";
        Httpreq.open("POST", Httpurl, true);

        Httpreq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        var tab_title = tab.title;
        Httpreq.onreadystatechange = function() {
            if (Httpreq.readyState == 4) {
                alert(Httpreq.responseText);
            }
        }

        json = {
            "uid": uid,
            "query": tab_title
        }

        Httpreq.send(json);
        alert("post sent!");
    });
}

window.onload=function() {
    var tab_title = document.title;
    if (tab_title == "Popup") {
        document.getElementById('query-highlight').addEventListener('click', queryHighlight);
        document.getElementById('query-title').addEventListener('click', queryTitle);
    } else if (tab_title == "Create") {
        document.getElementById('cbutton').addEventListener('click', createFunction);
    } else {
        document.getElementById('lbutton').addEventListener('click', loginFunction);
    }

}

