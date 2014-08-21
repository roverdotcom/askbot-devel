$(function() {
    if (!$('body').hasClass('js-app')) {
        return;
    }
    $('.js-send-to-phone-sms').autoDisableAjaxForm({
        error: function(xhr, statusText, httpStatusText, $form) {
            // Clear out any other alert containers
            $(".js-send-to-phone-message-container").children().remove();
            Rover.alerts.showAlert(
                'danger',
                xhr.responseJSON['message'],
                ".js-send-to-phone-message-container")
        },
        success: function(response, statusText, xhr, $form) {
            // Clear out any other alert containers
            $(".js-send-to-phone-message-container").children().remove();
            $('.js-send-to-phone-phone-number').val('');
            Rover.alerts.showAlert(
                'success',
                xhr.responseJSON['message'],
                ".js-send-to-phone-message-container")
        }
    });
});
