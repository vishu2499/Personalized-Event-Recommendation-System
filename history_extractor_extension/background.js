
// function sendHistoryToServerUsingGet(){

//     var xhttp = new XMLHttpRequest();
//     xhttp.onreadystatechange = function(){
//         alert(xhttp.responseText);
//     }

//     xhttp.open('POST','http://127.0.0.1:8000/recommender/index/',true);
//     // xhttp.open('GET','http://127.0.0.1:8000/recommender/index/',true);
//     xhttp.setRequestHeader('Content-type','application/x-www-form-urlencoded');
//     xhttp.send("director=zack_snyder");
// }


function sendHistoryToServerUsingPOST(historyJSON){

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        console.log(xhttp.responseText);
    }

    xhttp.open('POST','http://127.0.0.1:8000/recommender/index/',true);
    // xhttp.open('GET','http://127.0.0.1:8000/recommender/index/',true);
    xhttp.setRequestHeader('Content-type','application/json');
    xhttp.send(JSON.stringify(historyJSON));
}


function myData(data){
    historyJSON = [];
    moreData = {}
    moreData["user_id"] =  "2";
    historyJSON.push(moreData);

    var lastGotIT = false;
    var latestAccessedTime;

    data.forEach(function(page) {

        if(lastGotIT == false){
            latestAccessedTime = page.lastVisitTime;
        }

        console.log(page.title)
    
        singleHistory = {}
        singleHistory["title"] = page.title;
        singleHistory["time"] = page.lastVisitTime;
        singleHistory["url"] = page.url  ;
        historyJSON.push(singleHistory);
    });

    moreData = {}
    moreData["latestAccessedTime"] = latestAccessedTime;
    historyJSON.push(moreData);

    console.log(historyJSON);
    sendHistoryToServerUsingPOST(historyJSON);

}

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    // alert(`User ID from content js is Received ${msg} from ${sender.tab}, frame ${sender.frameId}`);
    // alert(`User ID from content js is Received ${JSON.stringify(msg)}`);
    var userId = msg["text"];

    chrome.history.search({text: '', maxResults: 9999999,startTime: 0}, function(data){
        historyJSON = [];
        temp = {}
        temp["user_id"] =  userId;
        historyJSON.push(temp);

        var lastGotIT = false;
        var latestAccessedTime;
    
        data.forEach(function(page) {

            if(lastGotIT == false){
                latestAccessedTime = page.lastVisitTime;
            }
        
            singleHistory = {}
            singleHistory["title"] = page.title;
            singleHistory["time"] = page.lastVisitTime;
            singleHistory["url"] = page.url  ;
            historyJSON.push(singleHistory);
        });

        // alert(latestAccessedTime);
        moreData = {}
        moreData["latestAccessedTime"] = latestAccessedTime;
        historyJSON.push(moreData);
    
        console.log(historyJSON);
        sendHistoryToServerUsingPOST(historyJSON);
    });
    sendResponse("something");
    
});

