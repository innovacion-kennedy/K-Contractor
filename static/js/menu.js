document.addEventListener("DOMContentLoaded", function () {
    let toggleBtn = document.querySelector('.base-toggle-btn');
    let sidebar = document.querySelector('.base-sidebar');
    let content = document.querySelector('.base-content');

    // Alternar menú lateral
    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle('collapsed');

        if (sidebar.classList.contains('collapsed')) {
            content.style.marginLeft = "0";
        } else {
            content.style.marginLeft = "200px";
        }
    });

    // Dropdown de usuario
    let userDropdown = document.querySelector(".user-dropdown-toggle");
    let dropdownMenu = document.querySelector(".dropdown-menu");

    userDropdown.addEventListener("click", function () {
        dropdownMenu.classList.toggle("show");
    });

    // Cerrar dropdown al hacer clic fuera
    document.addEventListener("click", function (event) {
        if (!userDropdown.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove("show");
        }
    });
});
