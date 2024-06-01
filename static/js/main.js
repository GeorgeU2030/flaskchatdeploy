export function mainjs (){
    return "ESTE ES EL MAIN.JS"
}

window.onload = function() {
    var result = mainjs();
    // Encuentra el elemento con el id "result" y actualiza su contenido
    document.getElementById("result").textContent = result;
}