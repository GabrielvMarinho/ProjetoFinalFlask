
function esperarElementoCarregar(selector, callback) {
    const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
            // O elemento foi encontrado, execute o callback
            callback(element);
            observer.disconnect(); // Parar de observar
        }
    });

    // Configuração do observer para observar mudanças no DOM
    observer.observe(document.body, { childList: true, subtree: true });
}
// Exemplo de uso:
esperarElementoCarregar(".modalFeedback", (element) => {
    element.classList.add("show")
    spanFeed = document.getElementsByClassName("spanFeedback")[0]
    spanFeed.onclick = function() {
        window.location.href = "/homeDependente";
    }
      
    
      // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target === element) {
            window.location.href = "/homeDependente";

    
        }
    }
    

    
});

// Quando checado um texto nas mensagens de erro ele chama
  // When the user clicks on <span> (x), close the modal




