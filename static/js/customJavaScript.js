

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendGetRequest(){

    var csrf_token = getCookie('csrftoken');

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function (){
        var myData = JSON.parse(this.responseText);
    }

    // xhttp.open('GET','/collector/test',true);

    xhttp.open('POST','/collector/put_evidence/',true);
    xhttp.setRequestHeader('X-CSRFToken',csrf_token);
    xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    xhttp.send('movie=justice_league&director=zack snyder');
}

function sendEvidenceToCollector(userid,eventid,evidenceType){
    // alert(`User: ${userid}\nEvent:${eventid}\nEvidence:${evidenceType}`);

    var csrf_token = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){

    }

    xhttp.open('POST','/collector/put_evidence/',true);
    xhttp.setRequestHeader('X-CSRFToken',csrf_token);
    xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    xhttp.send(`user=${userid}&eventid=${eventid}&evidenceType=${evidenceType}`);
}

function testRecommendation(){
    
}

function sendHistoryToServerUsingGet(){
    console.log("From inside send history to server")
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        alert(xhttp.responseText);
    }

    xhttp.open('GET','/recommender/index/',true);
    // xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
    xhttp.send();
}

function addContentToPage(content){
    var mainDiv = document.getElementById("personalized-div");

    var mainContent = "";


    content.forEach(function(item,index){

        console.log("from inside add content page:");
        console.log("Type of decription is");
        console.log(typeof item.description);

        var eachNode = `<div class="col-sm-4">
                    <div class="card" style="width: 18rem">
                    <img src="/static/${item.image_link}" class="card-img-top" alt="..." />
                    <div class="card-body">
                        <h5 class="card-title">${item.id} ${item.name}</h5>
                        <p class="card-text">${item.description.slice(0,20)}
                        </p>
                        <a href="/events/${item.id}/" onclick="sendEvidenceToCollector(${item.id},${item.user_id},4)" class="btn btn-primary">View More</a>
                    </div>
                    </div>
                </div>`;

        // console.log(`${eachNode}`);

        mainContent = mainContent.concat(eachNode);
    });

    console.log("Here is the main content")
    console.log(mainContent)
    mainDiv.innerHTML = mainContent;
}

function showAlert(){
    alert("Dummy method to show alert");
}

var myTimer
function startCalls(userid){
    console.log("Background call made for recommendations..");
    myTimer = setInterval(function() {
        
        // var csrf_token = getCookie('csrftoken');
        var xhttp = new XMLHttpRequest();
        xhttp.responseText = 'json';
        xhttp.onreadystatechange = function(){

            if(xhttp.readyState == 4 && xhttp.status == 200){
                var content = JSON.parse(this.responseText);
                
                addContentToPage(content);

                console.log("Times")
                content.forEach(function(item,index){
                    console.log(item)
                });

                stopCalls();
                // alert(JSON.stringify(content));

            }else if(xhttp.readyState == 4 && xhttp.status == 503){
                console.log(JSON.parse(this.responseText));
                console.log("Inside status code 503");  
            }
        }
    
        xhttp.open('POST','/recommender/history_recommendations/',true);
        // xhttp.setRequestHeader('X-CSRFToken',csrf_token);
        xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
        // alert(userid);
        xhttp.send(`user=${userid}`);

      }, 5000);
}

function stopCalls(){
    clearInterval(myTimer);
}


function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition,error);
    }else{
        alert("location not available");
    }
  }
  
function showPosition(position) {
    var hidden_location_field = document.getElementById("user_location");
    hidden_location_field.value = `${position.coords.latitude}--${position.coords.longitude}`;
    // alert("Location has been retreived",position.coords.latitude);
}

function error(err) {
    alert(`ERROR(${err.code}): ${err.message}`);
}

  