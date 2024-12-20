// Get modal and close button elements
const modalDeposito = document.getElementById("myModalDepo");
const spanDepo = document.getElementsByClassName("closeDepo")[0];


// Function to show the modal
function adicionarSaldoModal() {
    modalDeposito.classList.add("show");
}

spanDepo.onclick = function() {
    modalDeposito.classList.remove("show");
}

// Close the modal if the user clicks outside it
window.onclick = function(event) {
    if (event.target === modalDeposito) {
        modalDeposito.classList.remove("show");
    }
}

// Function to submit the deposit amount (optional functionality)
function submitDeposit() {
    const depositAmount = document.getElementById("depositAmount").value;
        fetch(`/adicionarSaldoResponsavel/${parseInt(depositAmount)}`, {
          method: 'POST', 
      })  .then(() => {

        modalDeposito.classList.remove("show");
        window.location.href = window.location.href


    });
}
