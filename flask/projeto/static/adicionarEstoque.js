// Get modal and close button elements
const modalEstoque = document.getElementById("myModalEstoque");
const spanEstoque = document.getElementsByClassName("closeEstoque")[0];
var idProd;

// Function to show the modal
function adicionarEstoqueModal(id) {
    idProd = id
    modalEstoque.classList.add("show");
}

spanEstoque.onclick = function() {
    modalEstoque.classList.remove("show");
}

// Close the modal if the user clicks outside it
window.onclick = function(event) {
    if (event.target === modalEstoque) {
        modalEstoque.classList.remove("show");
    }
}

// Function to submit the deposit amount (optional functionality)
function submitEstoque() {
    const depositAmount = document.getElementById("estoqueAmount").value;

    fetch(`/adicionarEstoqueFim/${parseInt(idProd)}/${parseInt(depositAmount)}`, {
          method: 'POST', 
      })  .then(() => {

        modalEstoque.classList.remove("show");
        window.location.href = window.location.href


    });
}
