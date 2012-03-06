// Upon opening Google Chrome,
// check if exam page exists.
// If it does, then grab its ID,
// select it, disallow switching,
// and delete any new tabs.

var checkTest = chrome.tabs.query({}, function(tabs) {
  for (var i = 0; i < tabs.length; i++) {
    // found exam
    if (tabs[i].url.indexOf('essaysafe.org/take') > 0 ||
	     tabs[i].url.indexOf('localhost:8080/take') > 0) { 
      alert("found tab");
      // select the exam tab
      chrome.tabs.update(tabs[i].id,{selected:true});
      // disallow switching tabs
      var active_listener = function(tabId, selectInfo) {
        chrome.tabs.update(tabs[i].id, {selected: true});
      };
      chrome.tabs.onActiveChanged.addListener(active_listener);
      
      var destroy_listener = function(tab) {
        chrome.tabs.remove(tab.id);
      };
      // delete any new tabs
      chrome.tabs.onCreated.addListener(destroy_listener);
      return;
    }
  }
  chrome.tabs.onCreated.removeListener(destroy_listener);
  chrome.tabs.onActiveChanged.removeListener(active_listener);
});

setInterval(checkTest, 1000);