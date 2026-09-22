document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.main-nav');

    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            const opened = nav.classList.toggle('is-open');
            toggle.setAttribute('aria-expanded', String(opened));
        });
    }

    const year = document.querySelector('[data-current-year]');
    if (year) {
        year.textContent = new Date().getFullYear();
    }
});
