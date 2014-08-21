$(function() {
    if (!$('body').hasClass('js-homepage')) {
        return;
    }

    var service = new google.maps.places.AutocompleteService(),
        geocoder = new google.maps.Geocoder();

    var getDisplayNameFromAutocompleteResult = function(result) {
        var description = result.terms[0].value + ', ' + result.terms[1].value;
        if (result.terms.length === 4) {
            description += ' ' + result.terms[2].value;
        }
        return description;
    };

    var getPlacePredictions = function(query, callback) {
        service.getPlacePredictions({
            input: query,
            types: ['geocode'],
            componentRestrictions: {country: 'us'}
        }, function(predictions, status) {
            if (status == google.maps.places.PlacesServiceStatus.OK) {
                callback($.map(predictions, getDisplayNameFromAutocompleteResult));
            }
        });
    };

    var reverseGeocodeAddress = function(address, callback) {
        geocoder.geocode({ address: address }, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                var lat = results[0].geometry.location.lat(),
                    lng = results[0].geometry.location.lng();
                callback(lat, lng);
            }
        });
    };

    var updateLatLngValues = function(lat, lng) {
        $('.js-lat').val(lat);
        $('.js-lng').val(lng);
    };

    var initializeLocationAutocomplete = function() {
        $('.js-location-input').typeahead({
            item: '<li><a class="needsclick" href="#"></a></li>',
            source: getPlacePredictions,
            autoSelect: false
        });
    };

    var initializeDatepicker = function() {
        $('.js-daterangepicker').daterangepicker({
            startElementSelector: '.js-start-date',
            endElementSelector: '.js-end-date'
        });
    };

    var geolocateUser = function() {
        Rover.geoIPLookup(function(lat, lng, name) {
            // Don't overwrite if the user is already searching
            if (!$('.js-location-input').val()) {
                $('.js-location-input').val(name);
                $('.js-lat').val(lat);
                $('.js-lng').val(lng);
            }
        });
    };

    var addUserDogsToSearchForm = function(dogs) {
        if (!dogs) {
            return;
        }
        var rendered = Mustache.template('new_design/dogs').render({
            dogs: dogs
        });
        $('.js-dog-list').html(rendered);
        $('.js-select-dogs').removeClass('hide');
    };

    var geocodeUserLocation = function() {
        var zip = Rover.person.get('zip');
        if (zip) {
            // Trigger a change to update the lat/lng values
            $('.js-location-input').val(zip).trigger("change");
        }
    };

    // Prevent prediction of likely service type (see method below) from
    // changing an already-selected state by the user
    var setStayTypeDirty = function() {
        $(this).data('dirty', true);
    };

    var preselectLikelyServiceType = function(home_stays_count, sitter_stays_count) {
        var $stayTypeSelector = $('.js-stay-type');
        if (sitter_stays_count > home_stays_count && !$stayTypeSelector.data('dirty')) {
            $stayTypeSelector.val('sitters');
        }
    };

    var getExtraDataFromUser = function() {
        $.ajax({
            url: Rover.urls.currentPersonExtraData,
            success: function(data) {
                addUserDogsToSearchForm(data.dogs);
                preselectLikelyServiceType(data.home_stays_count, data.sitter_stays_count);
            }
        });
    };

    var getPopupCookie = function(popupPk) {
        return $.cookie('geo_popup_' + popupPk);
    };

    var setPopupCookie = function(popupPk) {
        $.cookie('geo_popup_' + popupPk, 'dismissed', { expires: 90 });
    };

    var getGeoPromo = function() {
        var popupPk = Rover.utils.getUrlParameter('popup_pk');

        $.ajax({
            url: Rover.urls.homepageGeoPopupUrl,
            data: {
                popup_pk: popupPk
            },
            success: function(data) {
                if (data.popup) {
                    if (getPopupCookie(data.popupPk) && !data.debug) {
                        return;
                    }
                    $('.geo-popup-container iframe').attr('src', data.url);
                    $('.geo-popup-container').modal({show: true});
                    $('.geo-popup-container').on('hide.bs.modal', function() {
                        setPopupCookie(data.popupPk);
                    });
                }
            }
        });
    };

    var addSwipeToCarousel = function() {
        $('.carousel').swiperight(function() {
            $(this).carousel('prev');
        });

        $('.carousel').swipeleft(function() {
            $(this).carousel('next');
        });
    };

    var addBindings = function() {
        if (Rover.person.get('authenticated') === undefined) {
            $(window).on('authenticated.rover', getExtraDataFromUser);
            $(window).on('authenticated.rover', geocodeUserLocation);
        } else {
            if (Rover.person.isAuthenticated()) {
                getExtraDataFromUser();
                geocodeUserLocation();
            }
        }

        $('.js-location-input').on('change', function(event) {
            var val = $(this).val().trim();
            if (val) {
                reverseGeocodeAddress(val, updateLatLngValues);
            }
        });
        $('.js-stay-type').on('change', setStayTypeDirty);
        $('.js-more-about-booking').popover({
            html: true,
            placement: 'top',
            trigger: 'hover'
        });
    };

    var init = function() {
        initializeDatepicker();
        addBindings();
        addSwipeToCarousel();
        getGeoPromo();

        // optimizely test
        if (window.testLocationAutocomplete) {
            initializeLocationAutocomplete();
        }
    };

    init();
});
