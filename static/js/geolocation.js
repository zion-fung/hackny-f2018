function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude
    var longitude = position.coords.longitude;
    $.getJSON('/api/distance', {latitude: latitude, longitude: longitude}, function(data){});
}