Rover = Rover || {};
Rover.utils = Rover.utils || {};

$(function() {
    Rover.utils.isMobileBrowser = function() {
        return $('.js-mobile-test:visible').length === 1;
    };

    Rover.utils.isAndroid = function() {
        return (navigator.userAgent.match(/Android/i) !== null);
    };

    Rover.utils.isWindowsPhone = function() {
        return (navigator.userAgent.match(/Windows NT 6.2/i) !== null && navigator.userAgent.match(/Touch/i) !== null);
    };

    Rover.utils.isKindle = function() {
        return (navigator.userAgent.match(/\bSilk\/(.*\bMobile Safari\b)?/) || navigator.userAgent.match(/\bKF\w/) || navigator.userAgent.match('Kindle Fire'));
    };

    Rover.utils.isiOS = function() {
        return (navigator.userAgent.match(/iPhone|iPod/i) !== null || (navigator.userAgent.match(/iPad/)));
    };
});

Rover.utils.getUrlParameter = function(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
};

Rover.utils.hasHashParam = function(name) {
    if (window.location.hash) {
         var hash = window.location.hash.substring(1);
         if (hash.indexOf(name) != -1) {
            return true;
         }
    }
    return false;
};
