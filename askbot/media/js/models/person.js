Rover.models.person = Backbone.Model.extend({
    defaults: {
        authenticated: undefined,
        id: 0,
        homeSitter: false,
        travelingSitter: false,
        isSitter: false,
        listsAllServices: false,
        shortName: '',
        firstName: '',
        lastName: '',
        email: '',
        smallPhotoUrl: '',
        unreadMessageCount: 0,
        hasDogs: false,
        hasConnectedDevice: false,
        shouldPromptForPets: false,
        zip: '',
        timeZone: '',
        timeZoneOffset: '',
        newProfile: false
    },
    url: function() {
        return Rover.urls.currentPerson;
    },
    isAuthenticated: function() {
        return this.get('authenticated') === true;
    },
    isAnonymous: function() {
        return this.get('authenticated') === false;
    },
    isSitter: function() {
        return this.get('isSitter');
    },
    listsAllServices: function() {
        return this.get('listsAllServices');
    }
});

// Do this all very quickly, don't wait for document ready
(function() {
    var dataLayer = dataLayer || []; // Google Tag Manager (GTM)
    var fireAuthenticatedEvent = function() {
        if (Rover.person.isAuthenticated()) {
            $(window).trigger('authenticated.rover');
        } else {
            $(window).trigger('anonymous.rover');
        }

        if (Rover.person.isSitter()) {
            dataLayer.push({
                event: 'ownersitter',
                ownersitter: 'Sitter'
            });
        } else {
            dataLayer.push({
                event: 'ownersitter',
                ownersitter: 'Owner'
            });
        }
    };

    // var cacheUserData = function() {
    //     $.cookie('roverPerson', JSON.stringify(Rover.person.toJSON()), { path: '/' });
    // };

    var getPersonData = function() {
        Rover.person = new Rover.models.person();
        Rover.person.on('change:authenticated', fireAuthenticatedEvent);
        // Caching disabled for now, buggy implementation
        // if ($.cookie('roverPerson')) {
        //     Rover.person.set($.parseJSON($.cookie('roverPerson')));
        // } else {
        // $(window).on('authenticated.rover', cacheUserData);
        Rover.person.fetch();
        // }
    };

    var init = function() {
        getPersonData();
    };

    init();

})();