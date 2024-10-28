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

