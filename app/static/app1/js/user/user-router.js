'use strict';

angular.module('tyk-spike1')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/users', {
        templateUrl: 'views/user/users.html',
        controller: 'UserController',
        resolve:{
          resolvedUser: ['User', function (User) {
            return User.query();
          }]
        }
      })
    }]);
