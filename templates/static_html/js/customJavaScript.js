

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

        // console.log("from inside add content page:");
        // console.log("Type of decription is");
        // console.log(typeof item.description);
        console.log(item.category_image_link);
        alert(item.category_image_link);

        var eachNode = `<div class="col-sm-4">
                    <div class="card" style="width: 18rem">
                    <img src="${item.category_image_link}" class="card-img-top" alt="..." />
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
        xhttp.send(`user=${userid}`);

      }, 5000);
}

function stopCalls(){
    clearInterval(myTimer);
}
