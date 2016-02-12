(function() {
    var renderAuthenticatedHeader = function() {
        var isSitter = Rover.person.isSitter();

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

        var headerContext = {
            isSitter: isSitter,
            newProfile: Rover.person.get('newProfile'),
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
        };
        if(Rover.urls.settings) {
            headerContext.urlNotifications = appendURLRefHeader(Rover.urls.settings);
        }
        var rendered = Mustache.template('new_design/header/logged_in_user').render(headerContext);

        $(function() {
            if (!isSitter) {
                $('.js-become-a-sitter').removeClass('hide');
            } else if (!Rover.person.listsAllServices()) {
                $('.js-list-more-services').removeClass('hide');
            }
            $('.js-anonymous-header').html(rendered);
        });
    };

    var showHaveDogPrompt = function() {
        if (Rover.person.get('shouldPromptForPets') && !$.cookie('have_dog_prompt')) {
            $(function() {
                $('.js-have-dog-prompt').modal('show').on('hide.bs.modal', supressHaveDogPrompt);
            });
        }
    };

    var supressHaveDogPrompt = function() {
        $.cookie('have_dog_prompt', true, { expires: 3, path: '/' });
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

    var confirmNoDogs = function() {
        $.ajax(
            Rover.urls.hasDogs,
            {
                type: 'POST',
                data: {
                    'does_not_have_dogs': true
                },
                success: function() {
                    $('.js-have-dog-prompt .js-prompt').addClass('hidden');
                    $('.js-have-dog-prompt .js-thanks').removeClass('hidden');
                    window.setTimeout(function() {
                        $('.js-have-dog-prompt').modal('hide');
                    }, 3000);
                }
            }
        );
    };

    var confirmHasDogs = function() {
        suppressHaveDogPrompt();
        return true;
    };

    var addBindings = function() {
        $(function() {
            $('.js-app-download-link').on('click', trackAppDownloadLinkClick);
            $('.js-no-dog-link').on('click', confirmNoDogs);
            $('.js-has-dog-link').on('click', confirmHasDogs);
        });
    };

    var init = function() {
        addBindings();
        renderAuthenticatedHeader();
        showHaveDogPrompt();
    };

    if (Rover.person.isAuthenticated()) {
        init();
    } else {
        $(window).on('authenticated.rover', init);
    }
})();
