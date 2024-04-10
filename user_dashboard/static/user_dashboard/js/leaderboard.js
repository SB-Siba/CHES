function filterLeaderboard(city) {
    var rows = document.querySelectorAll('#leaderboard table tr[data-city]');
    rows.forEach(function(row) {
        if (city === 'all' || row.getAttribute('data-city') === city) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Event listener for the dropdown change event
document.getElementById('city-filter').addEventListener('change', function() {
    var selectedCity = this.value;
    // Filter leaderboard based on the selected city
    filterLeaderboard(selectedCity);
});