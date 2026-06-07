document.addEventListener("DOMContentLoaded", function () {
    
    const deleteButton = document.getElementById("delete");
    if (deleteButton) {
        const currentUrl = deleteButton.getAttribute("onclick");
        
        if (currentUrl) {
            deleteButton.removeAttribute("onclick");
            deleteButton.addEventListener("click", function (e) {
                const certeza = confirm("Tem a certeza absoluta que deseja eliminar este registo?");
                if (certeza) {
                    const urlPath = currentUrl.match(/'([^']+)'/)[1];
                    window.location.href = urlPath;
                }
            });
        }
    }

    const form = document.getElementById("form");
    if (form) {
        form.addEventListener("submit", function (e) {
            const inputs = form.querySelectorAll("input:not([readonly])");
            let valido = true;

            inputs.forEach(input => {
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
                e.preventDefault(); 
                
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
window.addEventListener('resize', function() {
    const plotlyPlots = document.querySelectorAll('.plotly-graph-div');
    
    plotlyPlots.forEach(function(plot) {
        if (window.Plotly) {
            window.Plotly.Plots.resize(plot);
        }
    });
});   
});
