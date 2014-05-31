var map;
function initialize() {
  var mapOptions = {
    zoom: 3,
    center: new google.maps.LatLng(-34.397, 150.644),
    mapTypeControl: false,
	panControl: false,
	scaleControl: false,
	overviewMapControl: false,
    zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL
    },
    streetViewControl: false
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);

