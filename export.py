use strict ;
use warnings ;
use autodie ;

use Net::Google::DataAPI::Auth::OAuth2 ;


my $oauth2 = Net::Google::DataAPI::Auth::OAuth2->new(
    client_id => 'xxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
    client_secret => 'mys3cr33333333333333t',
    scope => ['http://spreadsheets.google.com/feeds/'],

    # with web apps, redirect_uri is needed:
    #
    #   redirect_uri => 'http://your_app.sample.com/callback',

    );
my $url = $oauth2->authorize_url();

my $token = $oauth2->get_access_token($code) or die;

