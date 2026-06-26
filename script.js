document.addEventListener('DOMContentLoaded', () => {
    const categoryBtns = document.querySelectorAll('.category-btn');
    const backBtns = document.querySelectorAll('.back-btn');
    const mainNav = document.getElementById('main-nav');
    const contentSections = document.querySelectorAll('.content-section');
    const mainHeader = document.querySelector('.main-header');

    // Fonction globale pour refermer les accordéons
    function closeAllAccordions() {
        document.querySelectorAll('.accordion-content.w3-show').forEach(panel => {
            panel.classList.remove('w3-show');
            const btn = panel.previousElementSibling;
            if (btn) btn.classList.remove('w3-active');
        });
    }

    // 1. GESTION DU MENU PRINCIPAL (UE)
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            if (!targetSection) return;

            closeAllAccordions();

            if (btn.closest('#main-nav')) {
                mainNav.classList.add('zoomed-out');
                mainHeader.classList.add('hidden');
                document.body.classList.add('reading-mode'); // Active l'effacement du fond
            } else {
                btn.closest('.content-section').classList.remove('active');
            }

            setTimeout(() => {
                targetSection.classList.add('active');
                // REMONTE LA PAGE TOUT EN HAUT FLUIDEMENT
                window.scrollTo({ top: 0, behavior: 'smooth' }); 
            }, 300);
        });
    });

    // 2. GESTION DES PROJETS
    const projectCards = document.querySelectorAll('.project-card[data-target]');
    projectCards.forEach(card => {
        card.addEventListener('click', () => {
            const targetId = card.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                closeAllAccordions();
                
                // Masque l'UE actuellement ouverte SI le projet est dans une UE
                const currentUE = card.closest('.content-section');
                if (currentUE) {
                    currentUE.classList.remove('active');
                } else {
                    // SI on clique sur le projet depuis l'accueil directement !
                    mainNav.classList.add('zoomed-out');
                    mainHeader.classList.add('hidden');
                    document.body.classList.add('reading-mode'); // Efface tout le reste !
                }

                setTimeout(() => {
                    targetSection.classList.add('active');
                    // REMONTE LA PAGE TOUT EN HAUT FLUIDEMENT POUR VOIR LE PROJET
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }, 300);
            }
        });
    });

    // 3. GESTION DES BOUTONS DE RETOUR
    backBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentSection = btn.closest('.content-section');
            const targetBackId = btn.getAttribute('data-back');

            currentSection.classList.remove('active');

            setTimeout(() => {
                if (targetBackId === 'main-nav') {
                    mainNav.classList.remove('zoomed-out');
                    mainHeader.classList.remove('hidden');
                    document.body.classList.remove('reading-mode'); // Fait réapparaître le site
                    setTimeout(() => {
                        mainNav.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 100);
                } else {
                    // Retour à l'UE
                    const backSection = document.getElementById(targetBackId);
                    if (backSection) {
                        backSection.classList.add('active');
                        // Remonte en haut de l'UE
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                }
            }, 300);
        });
    });

    // 4. GESTION DES ACCORDÉONS
    document.querySelectorAll('.accordion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const panel = btn.nextElementSibling;
            if (!panel) return;

            const isOpen = panel.classList.contains('w3-show');
            const parentSection = btn.closest('.content-section');

            if (parentSection) {
                parentSection.querySelectorAll('.w3-show').forEach(openPanel => {
                    if (openPanel !== panel && openPanel.classList.contains('accordion-content')) {
                        openPanel.classList.remove('w3-show');
                        if (openPanel.previousElementSibling) {
                            openPanel.previousElementSibling.classList.remove('w3-active');
                        }
                    }
                });
            }

            panel.classList.toggle('w3-show', !isOpen);
            btn.classList.toggle('w3-active', !isOpen);
        });
    });
});