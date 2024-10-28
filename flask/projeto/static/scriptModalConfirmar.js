
const modal = document.getElementById("modalConfirmar");
var span = document.getElementsByClassName("close")[0];
var idProduto = null;

function confirmarExclusao(id){
    console.log("foi")
    document.getElementsByClassName("overlay")[0].classList.add("escuro");
    modal.style.display = "block";
    idProduto = id;
}
span.onclick = function() {
    document.getElementsByClassName("overlay")[0].classList.remove("escuro");
    modal.style.display = "none";
}
function confirmar(){
    fetch(`/removerProduto/${parseInt(idProduto)}`, {
        method: 'POST', 

    })
    location.reload();
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        document.getElementsByClassName("overlay")[0].classList.remove("escuro");

    }
}