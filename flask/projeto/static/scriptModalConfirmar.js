
var modalconf = document.getElementById("modalConfirmar");
var span = document.getElementsByClassName("close")[0];
var idProduto = null;

function confirmarExclusao(id, nome){
    document.getElementsByClassName("overlay")[0].classList.add("escuro");
    modalconf.style.display = "block";
    var textNome = document.getElementById("nomeProduto")
    console.log(nome)
    textNome.innerText = "Item: "+nome
    idProduto = id;
}
span.onclick = function() {
    document.getElementsByClassName("overlay")[0].classList.remove("escuro");
    modalconf.style.display = "none";
}
function confirmar(){
    fetch(`/removerProduto/${parseInt(idProduto)}`, {
        method: 'POST', 
    })
    location.reload();
}
