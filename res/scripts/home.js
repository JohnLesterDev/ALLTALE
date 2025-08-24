function main_home() {
    const mnCont = document.querySelector('.home-container');
    const logo = document.querySelector('.logo');
    const mainNavLinks = document.querySelectorAll('.main-nav ul li a');
    const modal = document.querySelector('.random-passage-modal');

    logo.addEventListener('click', () => {
        mnCont.classList.toggle('active');
        modal.classList.toggle('visible');
        modal.classList.toggle('hidden');

        logo.classList.toggle('active');
        mainNavLinks.forEach(link => link.classList.toggle('active'));
    });
}

main_home();