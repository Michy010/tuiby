function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;

                // Save to localStorage
                localStorage.setItem("latitude", lat);
                localStorage.setItem("longitude", lon);

                // Set hidden inputs
                document.getElementById("latitude").value = lat;
                document.getElementById("longitude").value = lon;

                // Get location name
                getLocationName(lat, lon);
            },
            function (error) {
                alert("Error getting location: " + error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function getLocationName(lat, lon) {
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            let city = data.address.city || data.address.town || data.address.village || data.address.municipality || 'City not found';
            
            // Save city in localStorage
            localStorage.setItem("city", city);

            // Set input value
            const locationInput = document.getElementById("seller-Location");
            locationInput.value = city;
            // locationInput.disabled = true;
        })
        .catch(error => console.error('Error:', error));
}

// Load saved location when page loads
document.addEventListener("DOMContentLoaded", function () {
    const savedCity = localStorage.getItem("city");
    const savedLat = localStorage.getItem("latitude");
    const savedLon = localStorage.getItem("longitude");

    if (savedCity && savedLat && savedLon) {
        document.getElementById("seller-Location").value = savedCity;
        document.getElementById('sellerLocationDisplay').textContent = savedCity;
        document.getElementById("seller-Location").disabled = true;
        document.getElementById("latitude").value = savedLat;
        document.getElementById("longitude").value = savedLon;
    }
});
