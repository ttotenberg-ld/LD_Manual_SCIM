# Manually Create LaunchDarkly User with the SCIM API

## Scope
This is a small example illustrating how you can create a LaunchDarkly user [using the SCIM API.](https://docs.launchdarkly.com/home/account-security/sso#user-provisioning-with-scim) It does 3 things:

1. Directs you to authorize your app with LaunchDarkly
1. Gets a token
1. Creates a user

This does NOT do anything else yet - such as getting a token for a new session, passing in different user credentials, or integrating with any particular IdP. It is just intended as a small example to help get you started, and show a bit of example data. Hope it helps! :)

## Usage

1. Make sure you have `pip install`ed all the dependencies
2. Replace `client_id`, `client_secret`, and `redirect_uri` with your values
3. Run the Python file to start the server
4. In a browser, go to (by default) http://localhost:5000/auth
