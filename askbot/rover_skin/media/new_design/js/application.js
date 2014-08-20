var Rover = Rover || {};

// Context for a given view goes here
Rover.context = Rover.context || {};


/**
 * Ensure that window always has the hasOwnProperty method on it, as
 * older versions of IE do not have this, and we are testing for jQuery presence
 * using it.
 */
window.hasOwnProperty = function(obj) {
    return (this[obj]) ? true : false;
};


/**
 * Prevent errors from calls to console.* from browsers that don't support it.
 */
if (!window.hasOwnProperty('console')) {
    window.console = {
        assert: function() {},
        clear: function() {},
        count: function() {},
        debug: function() {},
        dir: function() {},
        dirxml: function() {},
        error: function() {},
        exception: function() {},
        group: function() {},
        groupCollapsed: function() {},
        groupEnd: function() {},
        info: function() {},
        log: function() {},
        profile: function() {},
        profileEnd: function() {},
        table: function() {},
        time: function() {},
        timeEnd: function() {},
        timeStamp: function() {},
        trace: function() {},
        warn: function() {}
    };
}


(function() {

    /**
     * Extole + Optimizely
     *
     * window.roverExtoleZone, window.roverExtoleCampaignID, and window.roverExtoleElementID
     * are set in Optimizely and we dynamically create the extole/widget
     * script tag here, inserting it into the element specified by window.roverExtoleElementID
     * Note, it needs to be an ID instead of a class because IE8 doesn't have getElementByClassName support
     *
     */
    var initExtole = function() {
        if (window.roverExtoleZone && window.roverExtoleCampaignID && window.roverExtoleElementID && !window.roverExtoleInit) {
            window.roverExtoleInit = true;
            var containerElt = document.getElementById(window.roverExtoleElementID);
            if (!containerElt) {
                return;
            }

            var extoleScript = document.createElement('script');
            extoleScript.type = 'extole/widget';
            var contents = '{"zone": "' + window.roverExtoleZone + '", "campaignId" : "' + window.roverExtoleCampaignID + '", "params": {}}';
            extoleScript.text = contents;
            containerElt.parentNode.insertBefore(extoleScript, containerElt);
        }
    };

    initExtole();
})();

$(function() {

    var isRoverURL = function(url) {
        return url.indexOf('//') === -1 ||
            url.indexOf(Rover.urls.base) !== -1 ||
            url.indexOf('//localhost') !== -1 ||
            url.indexOf('//0.0.0.0') !== -1 ||
            url.indexOf('//127.0.0.1') !== -1;
    };

    // Send CSRF token in all ajax calls as a header
    $(document).ajaxSend(function(e, jqxhr, settings) {
        if (!$.cookie('csrftoken')) {
            return;
        }

        if (isRoverURL(settings.url)) {
            jqxhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    });

    var showAuthOnlyElements = function() {
        $('.js-authenticated-user').removeClass('hide');
    };

    var showAnonymousElements = function() {
        $('.js-anonymous-user').removeClass('hide');
    };

    var showModal = function() {
        var template = Mustache.template('new_design/common/modal'),
            rendered = template.render({
                content: $($(this).attr('data-target')).html(),
                title: $(this).attr('data-title'),
                classes: 'scrollable'
            });

        $('.js-app-modal').remove();
        $('body').append(rendered);
        $('.js-app-modal').modal('show');
    };

    var getWordCount = function(s) {
        s = s.replace(/(^\s*)|(\s*$)/gi,"");
        if (s === '') return 0;  // otherwise s.split().length will return 1 for a blank string
        return s.split(/\s+/).length;
    };

    var updateWordCount = function(e) {
        var $el = $(e.currentTarget);
        $el.siblings().find('.js-word-count-input-counter').html(getWordCount($el.val()));
    };

    var initWordCount = function() {
        $('.js-word-count-input').trigger('keyup');
    };

    /**
     * Use Bootstrap Popovers for the jQuery validation, as well as the
     * native Bootstrap validation, by adding `has-error` to the `.form-group`
     */
    var setValidationDefaults = function() {
        if (!$.isFunction($.validator)) {
            return;
        }
        $.validator.setDefaults({
            errorPlacement: function($error, $element) {
                var text = $error.text();
                if (text && text !== $element.data('currentText')) {
                    $element.popover('destroy');
                    $element.data('currentText', text);
                    $element.popover({
                        content: text,
                        trigger: 'manual',
                        placement: 'top',
                        template: '<div class="popover error-popover"><div class="arrow"></div><div class="popover-content"></div></div>'
                    });
                    $element.popover('show');
                    $element.parents('.form-group').addClass('has-error');
                } else if (!text) {
                    $element.data('currentText', '');
                    $element.parents('.form-group').removeClass('has-error');
                    $element.popover('destroy');
                }
            },
            success: function($element) {
                $element.popover('destroy');
            },
            invalidHandler: function(e, validator) {
                $(validator.currentForm).find('[type=submit]').prop('disabled', false);
            }
        });
    };

    var flagListing = function(e) {
        var $elt = $(e.currentTarget),
            url = $elt.attr('data-url'),
            path = $elt.attr('data-current-path'),
            content = $elt.attr('data-content');

        $elt.btn('loading');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                current_path: path,
                content: content
            },
            success: function() {
                $elt.btn('complete');
                // Need a small timeout, as triggering complete enables the button
                // on a timeout of 0
                setTimeout(function() {
                    $elt.prop('disabled', true);
                }, 2);
            }
        });
    };

    var disableClick = function() {
        return false;
    };

    var initializeGalleries = function() {
        var template = Mustache.template('new_design/social/modal_sharing_buttons');
        $('.js-image-gallery').each(function() {
            $(this).magnificPopup({
                delegate: 'a',
                type: 'image',
                image: {
                    markup: $.trim($('.js-photo-display-markup').html()),
                    cursor: null,
                    titleSrc: function() {
                        var $image = this.currItem.el,
                            shareLocation = $image.attr('data-share-location');

                        dataLayer.push({
                            event: 'large-photo-view',
                            share_location: shareLocation
                        });

                        return template.render({
                            imageToShare: $image.attr('data-image-to-share'),
                            imageThumbnail: $image.attr('data-image-thumbnail'),
                            urlToShare: $image.attr('data-url-to-share'),
                            contentType: $image.attr('data-content-type'),
                            objectId: $image.attr('data-object-id'),
                            campaign: $image.attr('data-campaign'),
                            trackingContent: $image.attr('data-tracking-content'),
                            caption: $image.attr('data-caption'),
                            shareLocation: shareLocation,
                            hideable: $image.attr('data-hideable') === 'true',
                            hidden: $image.attr('data-hidden') === 'true'
                        });
                    }
                },
                gallery: {
                    enabled: true
                }
            });
        });
        $('.js-shareable-image').on('mouseenter', function() {
            $(this).find('.js-hover-caption').addClass('in');
        }).on('mouseleave', function() {
            $(this).find('.js-hover-caption').removeClass('in');
        });
    };

    var initializeButtons = function() {
        var btn = $.fn.button.noConflict(); // reverts $.fn.button to jqueryui btn
        $.fn.btn = btn; // assigns bootstrap button functionality to $.fn.btn
        $('.rover-btn').btn();

        // Enable button toggling functionality for rover buttons. Bootstrap hardcodes
        // their listener on .btn, so we have to do the same for .rover-btn
        $(document).on('click.bs.button.data-api', '[data-toggle^="button"]', function(e) {
            var $roverBtn = $(e.target);

            // Account for the case when the click event occurred on something
            // inside the rover button
            if (!$roverBtn.hasClass('rover-btn')) {
                $roverBtn = $roverBtn.closest('.rover-btn');
            }

            $roverBtn.btn('toggle');
            e.preventDefault();
        });
    };

    var handleCalendarButtonClick = function(e) {
        e.preventDefault();
        var $this = $(this);
        var $trigger_target = $($this.attr('data-trigger-target'));
        if (!$trigger_target.length) {
            $trigger_target = $this.find('.js-date-picker');
        }
        $trigger_target.datepicker('show');
    };

    var addBindings = function() {
        if (Rover.person.get('authenticated') === undefined) {
            $(window).on('anonymous.rover', showAnonymousElements);
            $(window).on('authenticated.rover', showAuthOnlyElements);
        } else {
            if (Rover.person.isAuthenticated()) {
                showAuthOnlyElements();
            } else {
                showAnonymousElements();
            }
        }
        $(window).on('shown.shareable-image.rover', initializeGalleries);
        if ($.isFunction($.fancybox)) {
            $(document).on('click', '.fancybox-close', $.fancybox.close);
        }
        $('.js-show-modal').on('click', showModal);
        $('.js-disable-click').on('click', disableClick);
        $('.js-flag-listing').on('click', flagListing);
        $('.js-word-count-input').on('keyup', updateWordCount);
        $(document).on('click', '.js-datepicker-calendar-trigger', handleCalendarButtonClick);
    };

    var init = function() {
        addBindings();
        setValidationDefaults();
        initializeGalleries();
        initializeButtons();
        initWordCount();
    };

    init();
});

$(function() {
    var $html = $('html');
    if ($html.hasClass('ie9') || $html.hasClass('ie8') || $html.hasClass('ie7')) {
        $('input').placeholder();
    }
    /* Setup fastclick polyfill - see https://github.com/ftlabs/fastclick */
    FastClick.attach(document.body);
});

/***
 * Custom jQuery validators
 ****/
$.validator.addMethod('min_date', function(value, element, param) {
    return Date.parse(value) >= param;
});


$(function(){
    /**
     * Ajax support for carousel images.
     * Whenever a carousel slides, look for images in the
     * next slide that need to be loaded asynchronously.
     */
    $(document).on('slide.bs.carousel', '[data-ride="carousel"]', function(e){

        // Find the images in the the new slide that need loading
        var srcAttrName = 'data-src',
            loadingClass = 'rover-loading',
            $newSlide = $(e.relatedTarget),
            $imagesToProcess = $newSlide.find('img[' + srcAttrName + ']');

        $imagesToProcess.each(function(){
            // Find the image source that needs to be loaded
            var $img = $(this),
                newSrc = $img.attr(srcAttrName),
                $tmpImg = $('<img>');

            // Define behavior for when the image is finished loading
            $tmpImg.load(function(){
                $img.removeAttr(srcAttrName);
                $img.attr('src', newSrc);
                $img.unwrap();
            });

            // Update UI to reflect loading and start loading image
            $img.wrap('<div class="' + loadingClass + '"></div>');
            $tmpImg.attr('src', newSrc);
        });
    });
});
