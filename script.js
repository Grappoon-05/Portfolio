document.addEventListener('DOMContentLoaded', () => {
    const categoryBtns = document.querySelectorAll('.category-btn');
    const backBtns = document.querySelectorAll('.back-btn');
    const mainNav = document.getElementById('main-nav');
    const contentSections = document.querySelectorAll('.content-section');
    const mainHeader = document.querySelector('.main-header');

    function closeAllAccordions() {
        document.querySelectorAll('.accordion-content.w3-show').forEach(panel => {
            panel.classList.remove('w3-show');
            const btn = panel.previousElementSibling;
            if (btn) btn.classList.remove('w3-active');
        });
    }

    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            if (!targetSection) return;

            closeAllAccordions();

            if (btn.closest('#main-nav')) {
                mainNav.classList.add('zoomed-out');
                mainHeader.classList.add('hidden');
                document.body.classList.add('reading-mode');
            } else {
                btn.closest('.content-section').classList.remove('active');
            }

            setTimeout(() => {
                targetSection.classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' }); 
            }, 300);
        });
    });

    const projectCards = document.querySelectorAll('.project-card[data-target]');
    projectCards.forEach(card => {
        card.addEventListener('click', () => {
            const targetId = card.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                closeAllAccordions();
                
                const currentUE = card.closest('.content-section');
                if (currentUE) {
                    currentUE.classList.remove('active');
                } else {
                    mainNav.classList.add('zoomed-out');
                    mainHeader.classList.add('hidden');
                    document.body.classList.add('reading-mode');
                }

                setTimeout(() => {
                    targetSection.classList.add('active');
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }, 300);
            }
        });
    });

    backBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentSection = btn.closest('.content-section');
            const targetBackId = btn.getAttribute('data-back');

            currentSection.classList.remove('active');

            setTimeout(() => {
                if (targetBackId === 'main-nav') {
                    mainNav.classList.remove('zoomed-out');
                    mainHeader.classList.remove('hidden');
                    document.body.classList.remove('reading-mode');
                    setTimeout(() => {
                        mainNav.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 100);
                } else {
                    const backSection = document.getElementById(targetBackId);
                    if (backSection) {
                        backSection.classList.add('active');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                }
            }, 300);
        });
    });

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