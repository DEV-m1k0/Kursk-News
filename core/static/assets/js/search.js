const inpSearch = document.querySelector("#inpSearch")
const cards = document.querySelectorAll('#card')

inpSearch.addEventListener("input", (event) => {
    const inpValue = event.target.value.toString().toLowerCase()
    cards.forEach(card => {
        const cardTitle = card.querySelector('#card-title').innerHTML.toString().toLowerCase()
    
        if (cardTitle.includes(inpValue)) {
            card.classList.remove('d-none')
            card.classList.add('d-block')
        } else {
            card.classList.add('d-none')
            card.classList.remove('d-block')
        }
    
    });
})