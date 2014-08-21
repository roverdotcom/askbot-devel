/* GeoIPLookup performs a location lookup from the users IP. It uses our MaxMind
   database if possible, and if that doesn't work falls back to the new HTML5
   Geolocation (which requires a user to click an Allow button in their browser).

   You are expected to pass in callback functions to handle both success and failure
   cases:

   function successCallback(latitude, longitude, name)
   function errorCallback(error_message)
*/

var Rover = Rover || {};

$(function() {
    Rover.geoIPLookup = function(successCallback, errorCallback) {
        var ajaxLookupUrl =  '/ajax/geoip-lookup/';
        $.get(ajaxLookupUrl, function(result) {
            var name = '';
            if (result.status == 'success') {
                if (result.city && result.region) {
                    name = result.city + ", " + result.region;
                }
                if ($.isFunction(successCallback)) {
                    successCallback(result.latitude, result.longitude, name);
                }
            } else {
                // Fallback to HTML5 Geolocation
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            // Get City, State through extra call to google's Geocoder
                            if (!window.hasOwnProperty('google')) {
                                return;
                            }
                            var geocoder = new google.maps.Geocoder(),
                                latlng = new google.maps.LatLng(
                                    position.coords.latitude,
                                    position.coords.longitude);

                            geocoder.geocode({'latLng': latlng},
                                function(results, status) {
                                    if (status === google.maps.GeocoderStatus.OK) {
                                        var city = '',
                                            region = '',
                                            geocodeResult = results[0];
                                        for (var i=0; i<geocodeResult.address_components.length; i++) {
                                            if (geocodeResult.address_components[i].types[0] === "locality") {
                                                city = geocodeResult.address_components[i];
                                            }
                                            if (geocodeResult.address_components[i].types[0] === "administrative_area_level_1") {
                                                region = geocodeResult.address_components[i];
                                            }
                                        }
                                        name = city.long_name + ", " + region.short_name;
                                        if ($.isFunction(successCallback)) {
                                            successCallback(position.coords.latitude, position.coords.longitude, name);
                                        }
                                    }
                                }
                            );
                        },
                        function(error) {
                            switch(error.code) {
                                case error.PERMISSION_DENIED:
                                    msg = "PERMISSION_DENIED";
                                    break;
                                case error.POSITION_UNAVAILABLE:
                                    msg = "POSITION_UNAVAILABLE";
                                    break;
                                case error.TIMEOUT:
                                    msg = "TIMEOUT";
                                    break;
                                default:
                                    msg = "UNKNOWN_ERROR";
                                    break;
                            }
                            if ($.isFunction(errorCallback)) {
                                errorCallback(msg);
                            }
                        }
                    );
                } else {
                    if ($.isFunction(errorCallback)) {
                        errorCallback('GEOLOCATION_UNSUPPORTED');
                    }
                }
            }
        });
    };
});
