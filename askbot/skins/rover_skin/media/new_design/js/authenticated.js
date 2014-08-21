(function() {
    var renderAuthenticatedHeader = function() {
        var isSitter = Rover.person.isSitter();

        if (!isSitter) {
            $('.js-become-a-sitter').removeClass('hide');
        } else if (!Rover.person.listsAllServices()) {
            $('.js-list-more-services').removeClass('hide');
        }

        var truncateWithEllipsis = function(string, maxLength) {
            var ellipsis = '...';
            if (string.length > maxLength) {
                var truncateTo = maxLength - ellipsis.length;
                string = string.slice(0, truncateTo) + ellipsis;
            }
            return string;
        };

        var appendURLRefHeader = function(url) {
            var u = new Url(url);
            u.query.ref = "header";
            return u.toString();
        };

        var rendered = Mustache.template('new_design/header/logged_in_user').render({
            isSitter: isSitter,
            firstName: truncateWithEllipsis(Rover.person.get('firstName'), 12),
            smallPhotoUrl: Rover.person.get('smallPhotoUrl'),
            unreadMessageCount: Rover.person.get('unreadMessageCount'),

            urlOverview: appendURLRefHeader(Rover.urls.overview),
            urlDashboard: appendURLRefHeader(Rover.urls.dashboard),
            urlAccountEdit: appendURLRefHeader(Rover.urls.accountEdit),
            urlProfile: appendURLRefHeader(Rover.urls.profile),
            urlInbox: appendURLRefHeader(Rover.urls.inbox),
            urlCalendar: appendURLRefHeader(Rover.urls.calendar),
            urlLogout: appendURLRefHeader(Rover.urls.logout),
            urlDogPhotos: appendURLRefHeader(Rover.urls.dogPhotos),
            urlRebook: appendURLRefHeader(Rover.urls.rebook),

            hasDog: Rover.person.get('hasDogs'),
            canRebook: Rover.person.get('canRebook')
        });

        $('.js-anonymous-header').html(rendered);
    };

    var showAppDownloadPromo = function() {
        if (Rover.switches.isEnabled('app_download_promo') && Rover.person.isSitter() && !Rover.person.get('hasConnectedDevice') && !$.cookie('promote-app-download')) {
            dataLayer.push({'event': 'promote-app-download-shown'});
            $('.js-promote-app-download').modal('show').on('hide.bs.modal', function() {
                $.cookie('promote-app-download', true, { expires: 30, path: '/' });
            });
        }
    };

    var trackAppDownloadLinkClick = function(e) {
        var app = $(e.currentTarget).attr('data-which'),
            where = $(e.currentTarget).attr('data-where');
        if (where === 'modal') {
            dataLayer.push({'event': 'promote-app-download-clicked', 'app': app});
        } else if (where === 'conversation') {
            dataLayer.push({'event': 'conversation-app-download-clicked', 'app': app});
        }
    };

    var addBindings = function() {
        $('.js-app-download-link').on('click', trackAppDownloadLinkClick);
    };

    var init = function() {
        addBindings();
        renderAuthenticatedHeader();
        showAppDownloadPromo();
    };

    if (Rover.person.isAuthenticated()) {
        init();
    } else {
        $(window).on('authenticated.rover', init);
    }
})();
