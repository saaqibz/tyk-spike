'use strict';

angular.module('tyk-spike1')
  .factory('Item', ['$resource', 'localStorageService', function ($resource, localStorageService) {
    return $resource('http://tyk.docker:8080/restricted/api/items/:id', {}, {
      'query': { method: 'GET', isArray: true, transformRequest: addAuthToken},
      'get': { method: 'GET', transformRequest: addAuthToken},
      'save': { method: 'POST', transformRequest: addAuthToken}
    });


    function addAuthToken(data, headersGetter) {
		var token = localStorageService.get('apstoken');
	    if (token) {
	    	headersGetter()['Authorization'] = 'bearer ' + token;
	    }
	    return (angular.isObject(data)) ? JSON.stringify(data) : data;
    }
  }]);
