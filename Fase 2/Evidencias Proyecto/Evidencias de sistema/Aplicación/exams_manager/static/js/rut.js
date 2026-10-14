// ==================================================
// FORMATO AUTOMÁTICO DEL RUT (solo visual, sin validar el DV)
// Uso: aplicarFormatoRut(document.getElementById("rut"));
// ==================================================

function aplicarFormatoRut(inputRut) {

    if (!inputRut) {
        return;
    }

    // Deja solo números y una K final, con máximo 9 caracteres
    function limpiarRut(valor) {
        let limpio = valor.toUpperCase().replace(/[^0-9K]/g, "");
        const ultima = limpio.slice(-1);

        limpio = limpio.replace(/K/g, "") + (ultima === "K" ? "K" : "");

        return limpio.slice(0, 9);
    }

    // 12345678K -> 12.345.678-K
    function formatearRut(limpio) {
        if (limpio.length < 2) {
            return limpio;
        }

        const cuerpo = limpio.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, ".");

        return cuerpo + "-" + limpio.slice(-1);
    }

    // Cantidad de caracteres válidos antes del cursor
    function contarValidos(texto) {
        return texto.toUpperCase().replace(/[^0-9K]/g, "").length;
    }

    let anterior = limpiarRut(inputRut.value);

    inputRut.addEventListener("input", function (evento) {

        const cursor = inputRut.selectionStart;
        let posicion = contarValidos(inputRut.value.slice(0, cursor));
        let limpio = limpiarRut(inputRut.value);

        // Si se borró solo un punto o el guion, se borra el carácter vecino
        if (evento.inputType && evento.inputType.startsWith("delete") && limpio === anterior) {
            if (evento.inputType === "deleteContentBackward" && posicion > 0) {
                limpio = limpio.slice(0, posicion - 1) + limpio.slice(posicion);
                posicion -= 1;
            } else if (evento.inputType === "deleteContentForward") {
                limpio = limpio.slice(0, posicion) + limpio.slice(posicion + 1);
            }
            limpio = limpiarRut(limpio);
        }

        // Con el RUT completo, lo que se escriba de más no se agrega
        if (evento.inputType === "insertText" && anterior.length === 9 && contarValidos(inputRut.value) > 9) {
            limpio = anterior;
            posicion = Math.max(0, posicion - 1);
        }

        const formateado = formatearRut(limpio);
        inputRut.value = formateado;
        anterior = limpio;

        // Recoloca el cursor después del mismo número de caracteres válidos
        let nuevoCursor = 0;
        let vistos = 0;

        while (nuevoCursor < formateado.length && vistos < posicion) {
            if (/[0-9K]/.test(formateado[nuevoCursor])) {
                vistos += 1;
            }
            nuevoCursor += 1;
        }

        inputRut.setSelectionRange(nuevoCursor, nuevoCursor);
    });

    // Formatea un valor que el navegador haya rellenado al cargar
    inputRut.value = formatearRut(anterior);

}
