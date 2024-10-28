
var modal = document.getElementById("modalConfirmar");
console.log(modal)
var span = document.getElementsByClassName("close")[0];
var idProduto = null;

function confirmarExclusao(id, nome){
    document.getElementsByClassName("overlay")[0].classList.add("escuro");
    modal.style.display = "block";
    var textNome = document.getElementById("nomeProduto")
    console.log(nome)
    textNome.innerText = "Item: "+nome
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
