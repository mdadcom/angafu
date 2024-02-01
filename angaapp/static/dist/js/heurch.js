document.getElementById('id_destination').addEventListener('change', function() {
    var destinationId = this.value;
    var societeId = document.getElementById('id_societe').value;
    var car = document.getElementById('id_car').value; // Récupère la valeur de la car sélectionnée
    var heuresDepartSelect = document.getElementById('id_time');
    heuresDepartSelect.innerHTML = '';

    fetch('/get_heures_depart/?destination_id=' + destinationId + '&societe_id=' + societeId + '&car=' + car)
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
