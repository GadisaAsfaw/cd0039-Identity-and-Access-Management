/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'https://gadisasfaw-fsnd.us', // the auth0 domain prefix
    audience: 'gadisacfapi', // the audience set for the auth0 app
    clientId: '7wXkwxpKveWn3nnlQZHk5opZFcm4Heph', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8080/user-page', // the base url of the running ionic application. 
  }
};
