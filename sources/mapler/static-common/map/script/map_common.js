

function buildPoints(map, onPointClick) {
	$.each(pointsData, function( index, entry ) {
		var id = entry.id;
		var lng = entry.longitude;
		var lat = entry.latitude;
		var title = entry.description;
		var owner = entry.owner;
		var group = entry.group;
		var creationDate = entry.creationDate;

		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(lat, lng),
			map: map,
			title: owner + ' @ ' + group + '\n' + creationDate + '\n' + title
		});
		marker.mapler_id = id;

		google.maps.event.addListener(marker, 'click', function() {
			onPointClick(marker.mapler_id);
		});
	});
}

function initialize() {
	var mapOptions = {
		center: new google.maps.LatLng(50.43, 30.56),
		zoom: 11,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"),
	mapOptions);

	google.maps.event.addListener(map, "click", function (event) {
	    var latitude = event.latLng.lat();
		var longitude = event.latLng.lng();

		getMapOnClickCallback(latitude, longitude);
	});

	loadPointsData(function() {
		buildPoints(map, getPointOnClickCallback);
	});
	
}

google.maps.event.addDomListener(window, 'load', initialize);
