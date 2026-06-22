document.addEventListener('DOMContentLoaded', () => {
    const categoryBtns = document.querySelectorAll('.category-btn');
    const backBtns = document.querySelectorAll('.back-btn');
    const mainNav = document.getElementById('main-nav');
    const contentSections = document.querySelectorAll('.content-section');
    const mainHeader = document.querySelector('.main-header');

    // Pour chaque bouton de catégorie
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            // Vérifie si l'on est dans le menu principal ou dans une sous-section
            if (btn.closest('#main-nav')) {
                mainNav.classList.add('zoomed-out');
                mainHeader.classList.add('hidden');
                // Active le mode lecture : masque le reste de la page (À propos, Contact, footer...)
                document.body.classList.add('reading-mode');
            } else {
                // Cache la section parente actuelle si on clique depuis un sous-menu
                btn.closest('.content-section').classList.remove('active');
            }

            // Affiche la nouvelle section après un petit délai
            setTimeout(() => {
                targetSection.classList.add('active');
                // Replace le scroll en haut de la section pour une lecture propre
                targetSection.scrollTop = 0;
            }, 300);
        });
    });

    // Pour chaque bouton de retour
    backBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentSection = btn.closest('.content-section');
            const targetBackId = btn.getAttribute('data-back');

            // Cache la section courante
            currentSection.classList.remove('active');

            // Réaffiche la cible demandée (menu principal ou menu précédent)
            setTimeout(() => {
                if (targetBackId === 'main-nav') {
                    mainNav.classList.remove('zoomed-out');
                    mainHeader.classList.remove('hidden');
                    // Quitte le mode lecture : réaffiche le reste de la page
                    document.body.classList.remove('reading-mode');
                } else {
                    document.getElementById(targetBackId).classList.add('active');
                }
            }, 300);
        });
    });

    // Pour les boutons accordéons (Cours / SAÉ / Projets de chaque UE)
    document.querySelectorAll('.accordion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const panel = btn.nextElementSibling;
            const isOpen = panel.classList.contains('w3-show');

            panel.classList.toggle('w3-show', !isOpen);
            btn.classList.toggle('w3-active', !isOpen);
            btn.setAttribute('aria-expanded', String(!isOpen));
        });
    });
});