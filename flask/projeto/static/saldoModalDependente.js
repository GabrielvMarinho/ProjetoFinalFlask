// Get modal and close button elements
const modalDepositoDependente = document.getElementById("modalDepositoDependente");
const modalSaqueDependente = document.getElementById("modalSaqueDependente")
const spanDepoDep = document.getElementsByClassName("spanDepoDep")[0];
const spanRemovDep = document.getElementsByClassName("spanRemovDep")[0]

var idDependente;
// Function to show the modal

function adicionarSaldoModalDepo(id) {
    console.log("adicionar")
    idDependente = id
    modalDepositoDependente.classList.add("show");
    console.log("adicionar")

}
function retirarSaldoModalDepo(id){
        console.log("adicionar")

    idDependente = id
    modalSaqueDependente.classList.add("show")
}
spanRemovDep.onclick = function(){

    modalSaqueDependente.classList.remove("show")

}
spanDepoDep.onclick = function() {
    modalDepositoDependente.classList.remove("show");
}

// Close the modal if the user clicks outside it
window.onclick = function(event) {
    if (event.target === modalDepositoDependente ||event.target === modalSaqueDependente) {
        modalDepositoDependente.classList.remove("show")
        modalSaqueDependente.classList.remove("show")

    }

}

// Function to submit the deposit amount (optional functionality)
function Deposito() {
    const depositAmount = document.getElementById("depositAmountDepe").value;

        fetch(`/adicionarSaldo/${parseInt(depositAmount)}/${parseInt(idDependente)}`, {
          method: 'POST', 
      })  .then(() => {

        modalDepositoDependente.classList.remove("show");
        console.log("tirando aq")
        window.location.href = window.location.href

    });
}
function Saque(){
    const saqueAmountDepe = document.getElementById("saqueAmountDepe").value;

        fetch(`/removerSaldo/${parseInt(saqueAmountDepe)}/${parseInt(idDependente)}`, {
          method: 'POST', 
      })  .then(() => {

        modalSaqueDependente.classList.remove("show");
        console.log("tirando aq")
        window.location.href = window.location.href

    });
}
