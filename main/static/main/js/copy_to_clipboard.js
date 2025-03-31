function copyText() {
    let text = document.getElementById('textToCopy').innerText;

    let textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);

    textarea.select();
    document.execCommand('copy');

    document.body.removeChild(textarea);

    alert('Social media Handle copied!');
}