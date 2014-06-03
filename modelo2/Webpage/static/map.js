var map;
function initialize() {
  var mapOptions = {
    zoom: 1,
    center: new google.maps.LatLng(4.642425, -27.551018),
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
  var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
  
}

google.maps.event.addDomListener(window, 'load', initialize);

