(function() {
    var checkAndShowFacebookReturnClickSignupPromo = function() {
        var utmSource = Rover.utils.getUrlParameter('utm_source'),
            utmMedium = Rover.utils.getUrlParameter('utm_medium');

        // Came from a facebook share from our site
        if (utmSource === 'facebook' && utmMedium === 'onsite' && !Rover.state.autoOpenedPopup) {
            Rover.state.autoOpenedPopup = '.js-facebook-clickback-signup';
            setTimeout(showFacebookSignupPromo, 10000);
        }
    };

    var showFacebookSignupPromo = function() {
        $('.js-facebook-register input[name="promo_code"]').val(Rover.facebook.clickbackPromoCode);
        $('.js-facebook-clickback-signup').modal('show');
        dataLayer.push({'event': 'facebook-clickback-signup-modal-shown'});
    };

    var init = function() {
        checkAndShowFacebookReturnClickSignupPromo();
    };

    if (Rover.person.isAnonymous()) {
        init();
    } else {
        $(window).on('anonymous.rover', init);
    }
})();
