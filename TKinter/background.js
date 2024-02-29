chrome.runtime.onMessageExternal.addListener(function(message, sender, sendResponse) {
    if (message.action === 'openUrl') {
      var url = message.url;
      // Perform actions with the URL, e.g., open it in a new tab using Chrome API
      chrome.tabs.create({ url: url });
      sendResponse({ received: true });
    }
  });
  