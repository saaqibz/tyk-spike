'use strict';

angular.module('tyk-spike')
  .factory('User', ['$resource', function ($resource) {
    return $resource('api/users/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
