const modalConfirmarExcluConta = document.getElementById("modalConfirmarExcluConta");

const spanExcluConta = document.getElementsByClassName("spanExcluConta")[0];

function confirmarExclusao(){
    modalConfirmarExcluConta.classList.add("show")

}
window.onclick = function(event) {
    if (event.target === modalConfirmarExcluConta) {
        modalConfirmarExcluConta.classList.remove("show")

    }

}
spanExcluConta.onclick = function() {
    modalConfirmarExcluConta.classList.remove("show")
}
function confirmarExcluConta(){
    fetch(`/excluirContaPropria`, {
        method: 'POST', 
    })  .then(() => {
        window.location.href = window.location.href
    })
}

