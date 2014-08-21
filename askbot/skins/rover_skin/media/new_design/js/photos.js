$(function() {

    var hidePhoto = function(e) {
        var $hideButton = $(e.currentTarget);
        $hideButton.btn('loading');

        $.ajax({
            url: Rover.urls.hidePhotoUrl,
            type: 'POST',
            data: {
                'image_id': $hideButton.attr('data-object-id')
            },
            success: function() {
                toggleHiddenPhotoOnPage($hideButton.attr('data-hidden') === 'false', $hideButton);
            }
        });
    };

    var toggleHiddenPhotoOnPage = function(wasHidden, $buttonClicked) {
        var $photoOnPage = $('.js-shareable-image[data-object-id=' + $buttonClicked.attr('data-object-id') + ']');

        if (wasHidden) {
            $buttonClicked
                .attr('data-hidden', 'true')
                .btn('unhide');
            $photoOnPage
                .addClass('hidden-photo')
                .attr('data-hidden', 'true')
                .find('.js-hidden-photo').removeClass('hide');
        } else {
            $buttonClicked
                .attr('data-hidden', 'false')
                .btn('hide');
            $photoOnPage
                .removeClass('hidden-photo')
                .attr('data-hidden', 'false')
                .find('.js-hidden-photo').addClass('hide');
        }
    };

    var addBindings = function() {
        $(document).on('click', '.js-hide-photo', hidePhoto);
    };

    var init = function() {
        addBindings();
    };

    init();
});
