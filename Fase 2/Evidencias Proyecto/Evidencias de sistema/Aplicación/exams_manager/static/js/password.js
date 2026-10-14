// ==================================================
// MOSTRAR / OCULTAR CONTRASEÑA (botón de ojo)
// Uso: document.querySelectorAll(".toggle-password").forEach(aplicarMostrarPassword);
// ==================================================

function aplicarMostrarPassword(boton) {

    const input = document.getElementById(boton.getAttribute("aria-controls"));

    if (!input) {
        return;
    }

    boton.addEventListener("click", function () {
        const mostrar = input.type === "password";

        input.type = mostrar ? "text" : "password";
        boton.classList.toggle("is-visible", mostrar);
        boton.setAttribute("aria-label", mostrar ? "Ocultar contraseña" : "Mostrar contraseña");
    });

}
