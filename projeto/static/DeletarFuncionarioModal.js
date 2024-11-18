
const modalDelFunc = document.getElementById("modalConfirmarExcluFunc");

const spanExcluFunc = document.getElementsByClassName("spanExcluFunc")[0];
var idFunc = null;

function mostrarModalDeletar(id, nome){
    document.getElementsByClassName("overlay")[0].classList.add("escuro");
    modalDelFunc.style.display = "block";
    var textNome = document.getElementById("nomeProduto")
    console.log(nome)
    textNome.innerText = "Funcionário: "+nome
    idFunc = id;
}
window.onclick = function(event) {
    if (event.target === modalDelFunc) {
        modalDelFunc.classList.remove("show")

    }

}
spanExcluFunc.onclick = function() {
    document.getElementsByClassName("overlay")[0].classList.remove("escuro");
    modalDelFunc.style.display = "none";
}
function confirmarDelFunc(){
    fetch(`/removerFuncionario/${parseInt(idFunc)}`, {
        method: 'POST', 
    })

}
