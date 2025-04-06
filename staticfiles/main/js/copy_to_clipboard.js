function copyText(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(function () {
        alert("Copied: " + text);
    }, function (err) {
        alert("Failed to copy text");
    });
}