'use strict';

angular.module('tyk-spike')
  .controller('ItemController', ['$scope', '$modal', 'resolvedItem', 'Item', 'localStorageService',
    function ($scope, $modal, resolvedItem, Item, localStorageService) {

      $scope.items = resolvedItem;
      $scope.token = localStorageService.get('apstoken');

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.item = Item.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Item.delete({id: id},
          function () {
            $scope.items = Item.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Item.update({id: id}, $scope.item,
            function () {
              $scope.items = Item.query();
              $scope.clear();
            });
        } else {
          Item.save($scope.item,
            function () {
              $scope.items = Item.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.item = {
          
          "id": "",
          
          "name": "",
          
          "description": "",
          
          "thumbnail": "",          
        };
      };

      $scope.open = function (id) {
        var itemSave = $modal.open({
          templateUrl: 'item-save.html',
          controller: 'ItemSaveController',
          resolve: {
            item: function () {
              return $scope.item;
            }
          }
        });

        itemSave.result.then(function (entity) {
          $scope.item = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ItemSaveController', ['$scope', '$modalInstance', 'item',
    function ($scope, $modalInstance, item) {
      $scope.item = item;

      

      $scope.ok = function () {
        $modalInstance.close($scope.item);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
