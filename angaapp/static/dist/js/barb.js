// Importer Barba.js
import Barba from '@barba/core';

// Importer GSAP pour les animations (si nécessaire)
import gsap from 'gsap';

// Initialiser Barba.js
document.addEventListener('DOMContentLoaded', function() {
    Barba.init({
        transitions: [{
            name: 'fade',
            leave(data) {
                return gsap.to(data.current.container, { opacity: 0 });
            },
            enter(data) {
                return gsap.from(data.next.container, { opacity: 0 });
            }
        }]
    });

    // Définir des hooks de transition (facultatif)
    Barba.Dispatcher.on('initStateChange', function() {
        // Exécuter du code avant chaque transition de page
    });

    Barba.Dispatcher.on('newPageReady', function() {
        // Exécuter du code après chaque transition de page
    });
});
