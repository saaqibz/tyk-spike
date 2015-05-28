'use strict';

angular.module('tyk-spike')
  .factory('Item', ['$resource', 'localStorageService', function ($resource, localStorageService) {
  	var paramDefaults = {headers: {'authorization': 'bearer ' + localStorageService.get('apstoken')}};
    return $resource('http://tyk.docker:8080/restricted/api/items/:id', {}, {
      'query': { method: 'GET', isArray: true, transformRequest: addAuthToken},
      'get': { method: 'GET'},
      'update': { method: 'PUT'},
      'delete': { method: 'DELETE', transformRequest: addAuthToken}	
    });


	function addAuthToken(data, headersGetter) {
		var token = localStorageService.get('apstoken');
	    if (token) {
	    	headersGetter()['Authorization'] = 'bearer ' + token;
	    }
	    return data;
    }

  }]);
