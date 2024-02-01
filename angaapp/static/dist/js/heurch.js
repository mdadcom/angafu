document.getElementById('id_destination').addEventListener('change', function() {
    var destinationId = this.value;
    var societeId = document.getElementById('id_societe').value; // Récupère l'ID de la société sélectionnée
    var heuresDepartSelect = document.getElementById('id_time');
    heuresDepartSelect.innerHTML = ''; // Efface les anciennes options

    // Effectue une requête AJAX pour récupérer les heures de départ en fonction de la destination et de la société sélectionnées
    fetch('/get_heures_depart/?destination_id=' + destinationId + '&societe_id=' + societeId)
        .then(response => response.json())
        .then(data => {
            data.forEach(heure_depart => {
                var option = document.createElement('option');
                option.value = heure_depart.id;
                option.textContent = heure_depart.time;
                heuresDepartSelect.appendChild(option);
            });
        });
});