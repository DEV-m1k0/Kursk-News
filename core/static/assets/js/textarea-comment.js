// Optional character counter
const textarea = document.querySelector('.comment-textarea');
const footer = document.querySelector('.textarea-footer');

textarea.addEventListener('input', () => {
    const maxLength = 500;
    const currentLength = textarea.value.length;
    footer.setAttribute('data-count', `${currentLength}/${maxLength}`);
});