// Get modal and close button elements
const modalDepositoDependente = document.getElementById("modalDepositoDependente");
const spanDepoDep = document.getElementsByClassName("spanDepoDep")[0];
var action;
// Function to show the modal
console.log("modal =", modalDepositoDependente)

function adicionarSaldoModalDepo(action1) {

    console.log("modal =", modalDepositoDependente)
    action = action1
    modalDepositoDependente.classList.add("show");
}

spanDepoDep.onclick = function() {

    modalDepositoDependente.classList.remove("show");
}

// Close the modal if the user clicks outside it
window.onclick = function(event) {

    if (event.target === modalDepositoDependente) {
        modalDepositoDependente.classList.remove("show");
    }
}

// Function to submit the deposit amount (optional functionality)
function submitDeposit() {
    const depositAmount = document.getElementById("depositAmountDepe").value;
    console.log(depositAmount)

    if(action ==0){

    }
    else if(action == 1){

    }
        fetch(`/adicionarSaldoResponsavel/${parseInt(depositAmount)}`, {
          method: 'POST', 
      })  .then(() => {

        modalDepositoDependente.classList.remove("show");
        console.log("tirando aq")
        window.location.href = window.location.href


    });
}
