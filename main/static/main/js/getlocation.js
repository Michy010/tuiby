function getUserLocationAndSearch(event) {
    event.preventDefault(); // Prevent form from submitting immediately

    let query = document.getElementById("searchInput").value.trim();
    if (!query) {
        alert("Please enter a search term.");
        return;
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                let latitude = position.coords.latitude;
                let longitude = position.coords.longitude;

                // Redirect with query and location
                let searchUrl = `/filter_sellers/?query=${encodeURIComponent(query)}&latitude=${latitude}&longitude=${longitude}`;
                window.location.href = searchUrl;
            },
            function (error) {
                alert("Location access denied. Please allow location services.");
            }
        );
    } else {
        alert("Geolocation is not supported by your browser.");
    }
}

