const inpUserSearch = document.querySelector("#inpUserSearch");
const userCards = document.querySelectorAll('.user-card'); // Changed to class
const messageAlert = document.createElement('div'); // Create message element

// Add message element styling
messageAlert.className = 'alert alert-info mt-3 d-none';
messageAlert.textContent = 'Пользователи не найдены';
document.querySelector('.card-body').appendChild(messageAlert);

inpUserSearch.addEventListener("input", (event) => {
    const inpValue = event.target.value.trim().toLowerCase();
    let hiddenCount = 0;

    userCards.forEach(card => {
        const name = card.querySelector('.user-name').textContent.toLowerCase();
        const email = card.querySelector('.user-email').textContent.toLowerCase();
        const role = card.querySelector('.user-role').textContent.toLowerCase();

        const matches = name.includes(inpValue) || 
                        email.includes(inpValue) || 
                        role.includes(inpValue);

        card.style.display = matches ? 'block' : 'none';
        if (!matches) hiddenCount++;
    });

    // Show/hide no results message
    messageAlert.classList.toggle('d-none', hiddenCount !== userCards.length);
});