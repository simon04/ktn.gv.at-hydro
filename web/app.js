'use strict';

var App = angular.module('myApp', []).
controller('mainCtrl', ['$scope', function ($scope) {
  $scope.data = data;
  $scope.chart = [[[1,2],[3,4],[5,6]]];
}]);

App.directive('chart', function() {
  return {
    restrict: 'A',
    template: '<div></div>',
    replace: true,
    link: function(scope, elem, attrs) {
      var data = scope[attrs.ngModel];
      $.plot(elem, data, {
        xaxis: {show: false, ticks: 4},
        //yaxis: {show: false},
        grid: {show: true},
        colors: ['#f00']
});
    }
  };
});