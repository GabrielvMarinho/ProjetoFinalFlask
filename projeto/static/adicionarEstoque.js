// Get modal and close button elements
const modalEstoque = document.getElementById("myModalEstoque");
const modalEstoqueDel = document.getElementById("myModalEstoqueDelete");

const spanEstoque = document.getElementsByClassName("closeEstoque")[0];
var idProd;
const spanEstoqueDel = document.getElementsByClassName("closeEstoqueDel")[0];



function retirarEstoqueModal(id){
    idProd = id
    modalEstoqueDel.classList.add("show");
}
// Function to show the modal
function adicionarEstoqueModal(id) {
    idProd = id
    modalEstoque.classList.add("show");
}
spanEstoque.onclick = function() {
    modalEstoque.classList.remove("show");

}
spanEstoqueDel.onclick = function() {
    modalEstoqueDel.classList.remove("show");

}

// Close the modal if the user clicks outside it
window.onclick = function(event) {
    if (event.target === modalEstoque || event.target === modalEstoqueDel) {
        modalEstoque.classList.remove("show");
        modalEstoqueDel.classList.remove("show");

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



function submitEstoqueDelete() {
    const depositAmount = document.getElementById("estoqueAmountDelete").value;

    fetch(`/retirarEstoqueFim/${parseInt(idProd)}/${parseInt(depositAmount)}`, {
          method: 'POST', 
      })  .then(() => {

        modalEstoque.classList.remove("show");
        window.location.href = window.location.href


    });
}
