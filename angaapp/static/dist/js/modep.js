document.getElementById('reservationform').addEventListener('submit', function(event) {
    var modePaiementInputs = document.querySelectorAll('input[name="mode_paiement"]');
    var modePaiementSelected = false;

    // Vérifie si un mode de paiement est sélectionné
    modePaiementInputs.forEach(function(input) {
        if (input.checked) {
            modePaiementSelected = true;
        }
    });

    // Si aucun mode de paiement n'est sélectionné, affiche un message d'erreur
    if (!modePaiementSelected) {
        event.preventDefault(); // Empêche la soumission du formulaire

        var numTransInput = document.getElementById('num_trans');
        numTransInput.focus(); // Place le focus sur le champ de saisie du numéro de transfert
        numTransInput.style.borderColor = 'red'; // Change la couleur du bord du champ
        numTransInput.placeholder = 'Veuillez sélectionner un mode de paiement'; // Affiche le message d'erreur dans le champ
    }


});
