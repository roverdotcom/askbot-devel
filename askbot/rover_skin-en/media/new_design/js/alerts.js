$(function() {
    Rover.alerts = Rover.alerts || {};

    Rover.alerts.showAlert = function(severity, message, container) {
        if (_.indexOf(['success', 'info', 'warning', 'danger'], severity) === -1) {
            severity = 'info';
        }

        if (!container) {
            container = '.js-alerts-container';
        }

        var rendered = Mustache.template('new_design/common/alert').render({
            severity: severity,
            message: message
        });

        $(container).append(rendered);
    };
});
