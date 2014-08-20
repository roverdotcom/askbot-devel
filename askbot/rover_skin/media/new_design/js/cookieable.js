$(function() {
    var handleCookieableClick = function() {
        var $elt = $(this),
            cookieName = $elt.attr('data-cookieable-name'),
            expires = parseInt($elt.attr('data-cookieable-expires'), 10) || 7;

        if (cookieName) {
            $.cookie(cookieName, true, { expires: expires, path: '/' });
        }
    };

    $('.js-cookieable').on('click', handleCookieableClick);
});
