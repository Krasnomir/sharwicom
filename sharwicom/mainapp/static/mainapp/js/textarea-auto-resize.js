textarea = document.querySelector("textarea");
textarea.addEventListener('input', () => {autoResize(textarea)}, false);

window.addEventListener('load', () => {
    autoResize(textarea);
});

function autoResize(htmlTextarea) {
    console.log(htmlTextarea.scrollHeight);
    htmlTextarea.style.height = 'auto';
    htmlTextarea.style.height = htmlTextarea.scrollHeight + 'px';
}