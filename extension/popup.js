chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, "", function(response){
        chrome.identity.getProfileUserInfo(function(userInfo) {//https://stackoverflow.com/questions/28980582/chrome-extension-how-to-get-user-name
            // console.log("response from content script",response);
            //https://stackoverflow.com/a/56616752
            const bb = new Blob([response.reduce((prev, curr) => prev+`${curr[0]},${curr[1]}\n`,"")], { type: 'text/plain' });//https://stackoverflow.com/a/11083415
            const a = document.createElement('a');
            a.download = `${userInfo.id}.csv`;
            a.href = window.URL.createObjectURL(bb);
            a.click();
        });
    });
});
