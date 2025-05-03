const inpSearch = document.querySelector("#inpSearch")
const cards = document.querySelectorAll('#block-card')
const messageAlert = document.querySelector('#news-alert')


inpSearch.addEventListener("input", (event) => {
    const inpValue = event.target.value.toString().toLowerCase()
    let counter = 0

    cards.forEach(card => {
        const cardTitle = card.querySelector('#card-title').innerHTML.toString().toLowerCase()
    
        if (cardTitle.includes(inpValue)) {
            card.classList.remove('d-none')
            card.classList.add('d-block')
        } else {
            card.classList.add('d-none')
            card.classList.remove('d-block')
        }

        
        if (card.classList.contains('d-none')) {
            counter += 1
        } else {
            counter -= 1
        }


        if (counter == cards.length) {
            messageAlert.classList.remove('d-none')
        } else {
            messageAlert.classList.add('d-none')
        }
    
    });
})