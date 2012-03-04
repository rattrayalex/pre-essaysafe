// Upon opening Google Chrome,
// check if exam page exists.
// If it does, then grab its ID,
// select it, disallow switching,
// and delete any new tabs.

chrome.tabs.query({}, function(tabs) {
  for (var i = 0; i < tabs.length; i++) {
    // found exam
    if (tabs[i].url.indexOf('essaysafe.org/take') > 0 || 
	tabs[i].url.indexOf('localhost:8080/take') > 0) {
      // select the exam tab
      chrome.tabs.update(tabs[i].id,{selected:true});
      // disallow switching tabs
      chrome.tabs.onActiveChanged.addListener(function(tabId, selectInfo) {
        chrome.tabs.update(tabs[i].id, {selected: true});
      });
      
      // delete any new tabs
      chrome.tabs.onCreated.addListener(function(tab) {
        chrome.tabs.remove(tab.id);
      });
      break;
    }
  }
});
