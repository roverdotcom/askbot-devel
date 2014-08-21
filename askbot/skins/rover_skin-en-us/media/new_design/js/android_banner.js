$(function() {
    var showAndroidBanner = function() {
        if (!$.cookie('android-banner-dismissed')) {
            $('body').addClass('android-banner-shown');
        }
    };

    var hideBanner = function() {
        $('body').removeClass('android-banner-shown');
        $.cookie('android-banner-dismissed', true, { expires: 7, path: '/' });
    };

    var addBindings = function() {
        $('.js-dismiss-android-banner').on('click', hideBanner);
    };

    var init = function() {
        if (Rover.utils.isAndroid() && Rover.utils.isMobileBrowser()) {
            addBindings();
            showAndroidBanner();
        }
    };

    init();
});
