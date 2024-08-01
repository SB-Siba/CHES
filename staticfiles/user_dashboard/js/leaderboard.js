function filterLeaderboard(city) {
  var rows = document.querySelectorAll("#leaderboard table tr[data-city]");
  var topUserRow = rows[0]; // Assume the top user is the first row by default

  // Find the top user row if "All" is selected
  if (city === "all") {
    // No need to change topUserRow, already set to the first row
  } else {
    // Find the row with the highest points in the selected city
    rows.forEach(function (row) {
      if (row.getAttribute("data-city") === city) {
        if (
          !topUserRow ||
          parseInt(row.querySelector(".points").textContent) >
            parseInt(topUserRow.querySelector(".points").textContent)
        ) {
          topUserRow = row;
        }
      }
    });
  }

  // Show or hide rows based on the selected city
  rows.forEach(function (row) {
    if (city === "all" || row.getAttribute("data-city") === city) {
      row.style.display = ""; // Show the row
    } else {
      row.style.display = "none"; // Hide the row
    }
  });

  // Show the gold medal for the top user row and hide it for other rows
  rows.forEach(function (row) {
    var goldMedal = row.querySelector(".gold-medal");
    if (row === topUserRow && goldMedal) {
      goldMedal.style.display = ""; // Display gold medal for the top user
    } else {
      if (goldMedal) {
        goldMedal.style.display = "none"; // Hide gold medal for other users
      }
    }
  });
}

// Event listener for the dropdown change event
document.getElementById("city-filter").addEventListener("change", function () {
  var selectedCity = this.value;
  // Filter leaderboard based on the selected city
  filterLeaderboard(selectedCity);
});
