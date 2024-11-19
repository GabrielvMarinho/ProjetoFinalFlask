
const modalconf = document.getElementById("modalConfirmar");

const spanExclu = document.getElementsByClassName("spanExclu")[0];
var idProduto = null;

function confirmarExclusao(id, nome){
    document.getElementsByClassName("overlay")[0].classList.add("escuro");
    modalconf.style.display = "block";
    var textNome = document.getElementById("nomeProduto")
    textNome.innerText = "Item: "+nome
    idProduto = id;
}
window.onclick = function(event) {
    if (event.target === modalconf) {
        modalconf.classList.remove("show")

    }

}
spanExclu.onclick = function() {
    document.getElementsByClassName("overlay")[0].classList.remove("escuro");
    modalconf.style.display = "none";
}
function confirmar(){
    fetch(`/removerProduto/${parseInt(idProduto)}`, {
        method: 'POST', 
    })
    location.reload();
}
