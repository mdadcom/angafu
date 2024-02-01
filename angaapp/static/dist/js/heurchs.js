document.getElementById('id_destination').addEventListener('change', function() {
    var selectedDestination = this.value;
    var options = document.querySelectorAll('.heure_depart_option');

    // Masquer toutes les options d'heure de départ
    options.forEach(function(option) {
        option.style.display = 'none';
    });

    // Afficher les options correspondant à la destination sélectionnée
    if (selectedDestination) {
        var heuresDepartOptions = document.querySelectorAll('.heure_depart_option[data-destination="' + selectedDestination + '"]');
        heuresDepartOptions.forEach(function(option) {
            option.style.display = '';
        });
    }
});
