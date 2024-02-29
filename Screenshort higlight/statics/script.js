document.addEventListener('DOMContentLoaded', function() {
    const staticText = document.getElementById('static-text');
    const iframe = document.getElementById('displayed-url');

    staticText.addEventListener('mouseup', function() {
        const selection = window.getSelection().toString().trim();

        // Highlight the selected word in the static text
        highlightTextInStaticText(selection);

        // Send the selected word to the iframe for highlighting
        iframe.contentWindow.postMessage({ action: 'highlight', word: selection }, '*');
    });
});

// Listen for messages from the iframe
window.addEventListener('message', function(event) {
    if (event.data.action === 'highlight') {
        const highlightedWord = event.data.word;

        // Highlight the word in the static text
        highlightTextInStaticText(highlightedWord);

        // Highlight the word in the iframe content
        highlightTextInIframeContent(highlightedWord);
    }
});

function highlightTextInStaticText(word) {
    const staticTextElement = document.getElementById('static-text');
    const text = staticTextElement.innerText;

    const regex = new RegExp('\\b' + escapeRegExp(word) + '\\b', 'gi');

    staticTextElement.innerHTML = text.replace(regex, match => `<span class="highlighted">${match}</span>`);
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}


function highlightTextInIframeContent(word) {
    const iframeDocument = document.getElementById('displayed-url').contentDocument;
    const iframeBody = iframeDocument.body;

    iframeBody.innerHTML = iframeBody.innerHTML.replace(
        new RegExp('\\b' + escapeRegExp(word) + '\\b', 'g'),
        '<span class="highlighted">$&</span>'
    );
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
