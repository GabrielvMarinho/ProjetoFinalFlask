// Get modal and close button elements
const modalDeposito = document.getElementById("myModalDepo");
const spanDepo = document.getElementsByClassName("closeDepo")[0];
console.log(modalDeposito)
console.log(spanDepo)
// Function to show the modal
function adicionarSaldoModal() {
    modalDeposito.classList.add("show");
}

spanDepo.onclick = function() {
  document.getElementsByClassName("overlay")[0].classList.remove("escuro");
  modalconf.style.display = "none";
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
    console.log(depositAmount)
        fetch(`/adicionarSaldoResponsavel/${parseInt(depositAmount)}`, {
          method: 'POST', 
      })  .then(() => {

        modalDeposito.classList.remove("show");
        console.log("tirando aq")
        window.location.href = window.location.href


    });
}
