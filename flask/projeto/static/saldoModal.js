// Get the modal
const modalDeposito = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("btn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// Quando checado um texto nas mensagens de erro ele chama
function checarTexto(){
  const mensagens = document.getElementsByClassName("mensagensErro");
  if(mensagens.length>0){
    modalDeposito.classList.add("show")
  }
}
function adicionarSaldoModal(){
    
}
checarTexto();
  // When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modalDeposito.classList.remove("show")
  }
  

  // When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modalDeposito.classList.remove("show")

    }
}




