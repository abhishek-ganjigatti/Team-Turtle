let map;
let markers = [];
let heatmap;
let placesService;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: CONFIG.defaultLocation,
        zoom: CONFIG.defaultZoom
    });

    placesService = new google.maps.places.PlacesService(map);

    // Add click listener to map
    map.addListener('click', function(event) {
        searchNearbyPlaces(event.latLng);
    });

    // Add click listener to search button
    document.getElementById('searchButton').addEventListener('click', function() {
        this.disabled = true; // Disable the button
        this.textContent = "Searching..."; // Change button text
        searchNearbyPlaces(map.getCenter(), () => {
            this.disabled = false; // Re-enable the button
            this.textContent = "Search Places"; // Reset button text
        });
    });
}

function searchNearbyPlaces(location) {
    const radius = document.getElementById('radius').value;
    const placeType = document.getElementById('placeType').value;

    if (!radius || radius < 500 || radius > 5000) {
        alert("Please select a valid radius between 500 and 5000 meters.");
        return;
    }
    if (!placeType) {
        alert("Please select a valid place type.");
        return;
    }

    clearMarkers();
    
    const request = {
        location: location,
        radius: radius,
        type: placeType
    };

    placesService.nearbySearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            createHeatmap(results);
            displayPlaces(results);
        } else if (status === google.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
            alert("No results found.");
        } else {
            alert("Error fetching places: " + status);
        }
    });
}

function createHeatmap(places) {
    const heatmapData = places.map(place => ({
        location: place.geometry.location,
        weight: place.user_ratings_total || 1 // Use total ratings if available, otherwise default to 1
    }));

    if (heatmap) {
        heatmap.setMap(null);
    }

    heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: map
    });
}

function createMarker(place) {
    const iconColor = CONFIG.markerColors[document.getElementById('placeType').value] || '#000000'; // Default color if none is found
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: iconColor,
            fillOpacity: 0.6,
            strokeWeight: 0,
            scale: 10
        }
    });

    markers.push(marker);

    const infowindow = new google.maps.InfoWindow({
        content: `
            <div>
                <h3>${place.name}</h3>
                <p>Rating: ${place.rating || 'N/A'}</p>
                <p>${place.vicinity}</p>
            </div>
        `
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
}

function displayPlaces(places) {
    const placesList = document.getElementById('placesList');
    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found within the selected area.</p>';
    } else {
        places.forEach(place => {
            createMarker(place);

            const placeItem = document.createElement('div');
            placeItem.className = 'place-item';
            placeItem.innerHTML = `
                <h3>${place.name}</h3>
                <p>Rating: ${place.rating || 'N/A'}</p>
                <p>${place.vicinity}</p>
            `;
            placesList.appendChild(placeItem);
        });
    }
}
