document.addEventListener("DOMContentLoaded", function () {
    
    // 1. CONFIRMAÇÃO DE ELIMINAÇÃO
    const deleteButton = document.getElementById("delete");
    if (deleteButton) {
        // Removemos o comportamento inline temporariamente para aplicar o aviso
        const currentUrl = deleteButton.getAttribute("onclick");
        
        if (currentUrl) {
            deleteButton.removeAttribute("onclick");
            deleteButton.addEventListener("click", function (e) {
                const certeza = confirm("Tem a certeza absoluta que deseja eliminar este registo?");
                if (certeza) {
                    // Executa o link extraído do onclick original
                    const urlPath = currentUrl.match(/'([^']+)'/)[1];
                    window.location.href = urlPath;
                }
            });
        }
    }

    // 2. VALIDAÇÃO DINÂMICA DO FORMULÁRIO (Efeito visual ao tentar submeter vazio)
    const form = document.getElementById("form");
    if (form) {
        form.addEventListener("submit", function (e) {
            const inputs = form.querySelectorAll("input:not([readonly])");
            let valido = true;

            inputs.forEach(input => {
                // Ignorar validação da password no login.html se não for obrigatório mudar, 
                // mas valida campos de texto normais como nomes de diretor, universidade, etc.
                if (input.type !== "password" && input.value.trim() === "") {
                    valido = false;
                    input.style.borderColor = "#e74c3c";
                    input.style.backgroundColor = "#fdf2f2";
                } else {
                    input.style.borderColor = "#ddd";
                    input.style.backgroundColor = "#fff";
                }
            });

            if (!valido) {
                e.preventDefault(); // Trava o envio para o Flask
                
                // Procura ou cria um espaço de mensagem de erro
                let msgBox = document.querySelector(".msg");
                if (msgBox) {
                    msgBox.textContent = "Por favor, preencha todos os campos editáveis antes de salvar.";
                    msgBox.style.backgroundColor = "#fde8e8";
                    msgBox.style.color = "#e74c3c";
                    msgBox.style.display = "inline-block";
                }
            }
        });
    }
// 3. RESPONSIVIDADE DOS GRÁFICOS PLOTLY
// Deteta se a janela mudou de tamanho e força os gráficos a reajustarem-se ao layout CSS
window.addEventListener('resize', function() {
    // Procura todos os elementos de gráfico gerados pelo Plotly na página
    const plotlyPlots = document.querySelectorAll('.plotly-graph-div');
    
    plotlyPlots.forEach(function(plot) {
        // Se a biblioteca Plotly estiver carregada globalmente, faz o resize do gráfico
        if (window.Plotly) {
            window.Plotly.Plots.resize(plot);
        }
    });
});   
});