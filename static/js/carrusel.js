document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".login-image img");
    let currentIndex = 0;

    if (images.length === 0) {
        console.error("⚠ No se encontraron imágenes en .login-image");
        return;
    }

    function changeImage() {
        let currentImage = images[currentIndex];
        let nextIndex = (currentIndex + 1) % images.length;
        let nextImage = images[nextIndex];

        // 🔹 Quita la clase active de la imagen actual
        currentImage.classList.remove("active");

        // 🔹 Espera antes de mostrar la nueva imagen
        setTimeout(() => {
            nextImage.classList.add("active");
            currentIndex = nextIndex;
        }, 500); // Tiempo de la animación
    }

    // 🔹 Cambia la imagen cada 4 segundos
    setInterval(changeImage, 3500);
});
