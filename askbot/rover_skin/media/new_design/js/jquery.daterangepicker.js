/**
 * Date Range Picker, a jQuery UI datepicker wrapper
 * Author: Chris Roby
 * Copyright: © 2013 A Place For Rover, Inc.
 * License: MIT
 *
 * A simple jQuery UI datepicker wrapper that takes two required arguments,
 * startElementSelector and endElementSelector, along with a shared parent
 * element of both (to allow mulitple per page), and turns them into a tool
 * for selecting a date range. After a start date is selected, the end date
 * automatically is opened. Then, whenever the start date is changed afterwards,
 * the end date is opened up again automatically.
 *
 * This takes all of the arguments that the jQuery UI datepicker takes, with
 * some defaults that are specific to picking a date range
 *
 * Implementation notes:
 * If you use multiple on the same page, ensure that the IDs of each startElt
 * and endElt are different on the page.
 */

(function($) {
    $.fn.daterangepicker = function(options) {
        if (!(options.startElementSelector && options.endElementSelector)) {
            if (window.hasOwnProperty('console')) {
                console.warn('daterangepicker improperly configured');
            }
            if (window.hasOwnProperty('Raven')) {
                Raven.captureMessage('daterangepicker improperly configured');
            }
            return this;
        }

        options = $.extend({}, {
            minDate: new Date(),
            defaultStartDate: '+0d',
            defaultEndDate: '+3d',
            changeMonth: false,
            numberOfMonths: 1
        }, options);

        return this.each(function() {
            var $startElt = $(this).find(options.startElementSelector),
                $endElt = $(this).find(options.endElementSelector);

            var triggerOpened = function() {
                $(this).trigger('datepickerOpened');
            };

            var startEltOptions = $.extend({}, options, {
                onClose: function(selectedDate) {
                    if ($(this).data('newDate')) {
                        $(this).data('newDate', false);
                        $endElt.datepicker('option', 'minDate', selectedDate);
                        // Need to delay this focus, or a strange behavior happens
                        // where when you try to select the next month in the
                        // $endElt, it closes and re-opens
                        window.setTimeout(function() {
                            $endElt.focus();
                            $startElt.trigger('closed.datepicker');
                        }, 10);
                    }
                },
                onSelect: function(selectedDate) {
                    if ($(this).data('selectedDate') !== selectedDate) {
                        $(this).data('newDate', true);
                        $(this).data('selectedDate', selectedDate);
                        $startElt.trigger('change');
                    }
                }
            });

            $startElt.datepicker(startEltOptions);

            var endEltOptions = $.extend({}, options, {
                onClose: function(selectedDate) {
                    $endElt.trigger('closed.datepicker');
                }
            });

            $endElt.datepicker(endEltOptions);
        });
    };
}(jQuery));
