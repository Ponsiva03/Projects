document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('openUrlBtn').addEventListener('click', function() {
      chrome.runtime.sendMessage({ action: 'openUrl', url: 'https://www.example.com' }, function(response) {
        if (response && response.received) {
          console.log('URL sent to extension.');
        }
      });
    });
  });
  