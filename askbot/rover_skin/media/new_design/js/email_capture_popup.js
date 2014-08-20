$(function() {
    if (!$('.js-email-capture-popup').length) {
        return;
    }

    var cookieName = 'email_capture_popup';

    var doNotShowAgain = function() {
        $.cookie(cookieName, 'dismissed', {
            expires: 365,
            path: '/'
        });
    };

    var showThanks = function() {
        doNotShowAgain();
        $('.js-email-capture-popup-initial').fadeOut('fast', function() {
            $('.js-email-capture-popup-thanks').fadeIn('fast');
        });
    };

    var showPopup = function() {
        $.fancybox(
            $('.js-email-capture-popup-container').html(),
            {
                onClosed: doNotShowAgain
            }
        );

        $('.js-email-capture-form').ajaxForm({
            success: showThanks,
            error: showThanks
        });
    };

    var checkAndShowPopup = function() {
        if ($.cookie(cookieName) !== 'dismissed' && !Rover.utils.isMobileBrowser()) {
            Rover.state.autoOpenedPopup = '.js-email-capture-popup-container';
            if ($('.js-email-capture-popup-container').attr('data-style') === 'delayed') {
                setTimeout(function() {
                    if (!Rover.state.autoOpenedPopup) {
                        showPopup();
                    }
                }, 15000);
            } else {
                showPopup();
            }
        }
    };

    var init = function() {
        checkAndShowPopup();
    };

    init();
});
