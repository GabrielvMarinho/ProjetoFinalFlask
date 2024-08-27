let count = 1;  // Inicia o contador com 1

function updateDisplay() {
    document.getElementById('counter').innerText = count;
    document.getElementById('counter').value = count;
    document.getElementById('counter_value').value = count;
}

function increment() {
    if(count !=10){
        count++;
        updateDisplay();
    }
    
}

function decrement() {
    if(count !=1){
        count--;
        updateDisplay();
    }
    
    
}

// Inicializa a exibição do contador
updateDisplay();

// Inicializa a exibição do contador
updateDisplay();

// Obtém o modal
var modal = document.getElementById("myModal");

// Obtém o botão que abre o modal
var btn = document.getElementById("openModalBtn");

// Obtém o elemento <span> que fecha o modal
var span = document.getElementsByClassName("close")[0];

// Quando o usuário clicar no botão, abre o modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// Quando o usuário clicar no <span> (x), fecha o modal
span.onclick = function() {
    modal.style.display = "none";
}

// Quando o usuário clicar fora do modal, fecha o modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
