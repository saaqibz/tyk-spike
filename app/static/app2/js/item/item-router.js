'use strict';

angular.module('tyk-spike')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/items', {
        templateUrl: 'views/item/items.html',
        controller: 'ItemController',
        resolve:{
          resolvedItem: ['Item', function (Item) {
            return Item.query();
          }]
        }
      })
    }]);
