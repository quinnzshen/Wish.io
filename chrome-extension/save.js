window.addEventListener("load", windowLoaded, false);
function windowLoaded() {
  chrome.tabs.getSelected(null, function(tab) {
    document.getElementById('currentLink').innerHTML = tab.url;
    console.log(tab.url);
    chrome.tabs.create({
    	selected: true,
    	url: "http://127.0.0.1:8000"
    })
  });
}