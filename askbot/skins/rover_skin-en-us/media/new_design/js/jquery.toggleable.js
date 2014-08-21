$(function() {
    var toggleVisible = function(e) {
        var $currentTarget = $(e.currentTarget),
            toggleOff = $currentTarget.attr('data-toggle-off'),
            toggleOn = $currentTarget.attr('data-toggle-on'),
            $toggleOff = $(toggleOff),
            $toggleOn = $(toggleOn),
            fadedIn = false;

        var showToggleOnElts = function() {
            // because the callback is called for each element hidden, we
            // need to keep track and only toggle once
            if (!fadedIn) {
                fadedIn = true;
                if (!$toggleOn.is(':visible')) {
                    $toggleOn.hide().removeClass('hide').fadeIn('fast');
                }
                $(window).trigger('toggle-fired', {on: toggleOn, off: toggleOff});
            }
        };

        if ($toggleOff.length) {
            $toggleOff.fadeOut('fast', function() {
                $(this).addClass('hide');
                showToggleOnElts();
            });
        } else {
            showToggleOnElts();
        }
    };

    $('.js-toggle').on('click', toggleVisible);
});
