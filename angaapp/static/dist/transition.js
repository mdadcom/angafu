// transition.js
document.addEventListener('DOMContentLoaded', function() {
    // Sélectionnez votre indicateur de chargement
    const loader = document.getElementById('loader');

    Barba.init({
        transitions: [{
            name: 'fade',
            leave(data) {
                // Affichez l'indicateur de chargement avant de quitter la page actuelle
                loader.style.display = 'block';
                return gsap.to(data.current.container, { opacity: 0 });
            },
            enter(data) {
                // Masquez l'indicateur de chargement après l'entrée dans la nouvelle page
                loader.style.display = 'none';
                return gsap.from(data.next.container, { opacity: 0 });
            }
        }]
    });

    // Définissez des hooks de transition supplémentaires si nécessaire
});
