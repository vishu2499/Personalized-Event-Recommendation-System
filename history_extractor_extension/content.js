var userHiddenField = document.getElementById("user_id_hidden_field");

if(userHiddenField.value != 'not_logged'){
    // alert(`User ID is ${userHiddenField.value}`);
    chrome.runtime.sendMessage({text: userHiddenField.value}, function(response) {
        console.log(`${response}`)
    });
}






// var theHeader = document.getElementById("wargames");
// theHeader.innerHTML = "THe content is changed from content.js";
// alert(theHeader.innerHTML);