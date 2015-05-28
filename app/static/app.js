// Declare app level module which depends on filters, and services
angular.module('app-nav', ['LocalStorageModule'])
  .controller('NavCtrl', ['$http', 'localStorageService', '$timeout', function($http, localStorageService, $timeout){
  	var ctrl = this;
  		ctrl.token = localStorageService.get('apstoken');
	console.log('token:' + ctrl.token);

  	ctrl.submit = function(){
		var url = '//tyk.docker:8080/auth/login',
			data = {email: ctrl.email, password: ctrl.password},
			config = {
				headers: {'Content-Type': 'application/json'},
			}
		$http.post(url, data, config).then(function success(resp){
			ctrl.token = resp.data.token;
			localStorageService.set('apstoken', ctrl.token);
			console.log('Cookie:' + localStorageService.get('apstoken'));
		});
  	};

  }]);