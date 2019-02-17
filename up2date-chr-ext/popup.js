var uid = "-LYshCmequUOw-w7wAgG";

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
            uid = Httpreq.responseText;
            alert(Httpreq.responseText);
            console.log(uid);
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

window.onload=function() {
    var tab_title = document.title;
    if (tab_title == "Popup") {
        document.getElementById('query-highlight').addEventListener('click', queryHighlight);
        document.getElementById('query-title').addEventListener('click', queryTitle);
    } else if (tab_title == "Create") {
        document.getElementById('cbutton').addEventListener('click', createFunction);
    } else if (tab_title == "queries"){
        displayQueries();
    } else {
        document.getElementById('lbutton').addEventListener('click', loginFunction);
    }

}

