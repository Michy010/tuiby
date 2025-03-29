function getLocation(event) {
    if (event) event.preventDefault(); 

    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                let data = {
                    'latitude': position.coords.latitude,
                    'longitude': position.coords.longitude
                };

                fetch('/send-location/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(result => alert('Success:', result))
                .catch(error => console.error('Error:', error));
            },
            function (error) {
                alert('Error obtaining location:', error.message);
            }
        );
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}
