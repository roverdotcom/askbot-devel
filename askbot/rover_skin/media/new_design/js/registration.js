$(function() {
    if (!$('body').hasClass('js-registration')) {
        return;
    }

    var handleFacebookSignInError = function() {
        Rover.alerts.showAlert('danger', 'We were unable to sign you in with your Facebook account. Please sign in using your email address below.');
    };

    var facebookSignIn = function() {
        dataLayer.push({event: 'facebook-sign-in-button-clicked'});
        Rover.facebook.signup(false, handleFacebookSignInError);
    };

    var handleFacebookSignUpError = function() {
        Rover.alerts.showAlert('danger', 'We were unable to connect with Facebook. Please use the form below to sign up.');
    };

    var facebookSignUp = function() {
        dataLayer.push({event: 'facebook-sign-up-button-clicked'});
        Rover.facebook.signup(false, handleFacebookSignUpError);
    };

    var fireAnalyticsForToggle = function(e, data) {
        if (data.on === '.js-sign-in') {
            dataLayer.push({event: 'sign-in-toggle-clicked'});
            dataLayer.push({event: 'sign-in-page-view'});
        } else if (data.on === '.js-sign-up') {
            dataLayer.push({event: 'sign-up-toggle-clicked'});
            dataLayer.push({event: 'sign-up-page-view'});
        }
    };

    var fireAnalyticsForSubmit = function(e) {
        if ($(e.currentTarget).hasClass('js-sign-up-form')) {
            dataLayer.push({event: 'sign-up-button-clicked'});
        } else {
            dataLayer.push({event: 'sign-in-button-clicked'});
        }
    };

    var initializeValidation = function() {
        $('.js-sign-in-form').roverValidate();
        $('.js-sign-up-form').roverValidate({
            rules: {
                email: {
                    required: true,
                    email: true,
                    remote: {
                        url: Rover.urls.validateEmail,
                        type: 'GET'
                    }
                },
                zip_code: {
                    required: true,
                    zipcodeUS: true,
                    remote: {
                        url: Rover.urls.validateZipcode,
                        type: 'GET'
                    }
                }
            }
        });
    };

    var fireAnalyticsEvents = function() {
        if ($('.js-sign-up').hasClass('hide')) {
            dataLayer.push({event: 'sign-in-page-view'});
        } else {
            dataLayer.push({event: 'sign-up-page-view'});
        }
    };

    var addBindings = function() {
        $('.js-facebook-sign-up').on('click', facebookSignUp);
        $('.js-facebook-sign-in').on('click', facebookSignIn);
        $('.js-sign-up-form, .js-sign-in-form').on('submit', fireAnalyticsForSubmit);
        $(window).on('toggle-fired', fireAnalyticsForToggle);
    };

    var init = function() {
        addBindings();
        initializeValidation();
        fireAnalyticsEvents();
    };

    init();
});
