let estudioId = null;

async function analizar() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Seleccione una imagen");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Vista previa imagen
    document.getElementById("preview").innerHTML =
        `<img src="${URL.createObjectURL(file)}" style="max-width:300px;">`;

    try {
        const response = await fetch("/analizar", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Error en el servidor");
        }

        const data = await response.json();

        console.log("Respuesta backend:", data); // 🔎 DEBUG

        estudioId = data.estudio_id;

        // 👉 AQUÍ se muestra el informe (esto faltaba)
        document.getElementById("informe").innerHTML =
            marked.parse(data.informe);

        document.getElementById("resultado").classList.remove("hidden");

    } catch (error) {
        console.error(error);
        alert("Error al analizar la imagen");
    }
}

async function validar() {
    const estado = document.getElementById("estado").value;
    const diagnostico = document.getElementById("diagnostico").value;
    const comentario = document.getElementById("comentario").value;

    const formData = new FormData();
    formData.append("estudio_id", estudioId);
    formData.append("estado", estado);
    formData.append("diagnostico", diagnostico);
    formData.append("comentario", comentario);

    try {
        await fetch("/validar", {
            method: "POST",
            body: formData
        });

        alert("Validación guardada correctamente");

    } catch (error) {
        console.error(error);
        alert("Error al guardar validación");
    }
}
