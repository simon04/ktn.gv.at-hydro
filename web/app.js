'use strict';

var App = angular.module('myApp', []).
controller('mainCtrl', ['$scope', '$http', function ($scope, $http) {
  $scope.data = $http.get('http://localhost:8281/stations').then(function(d) {
    return d.data.stations.map(function(s) {
      s.plotdata = $scope.getSeriesForChart(s.station, 'w');
      return s;
    });
  });
  $scope.getSeriesForChart = function(sta, wq) {
    return $http.get('http://localhost:8281/stations/' + sta).then(function(d) {
      return d.data.data.map(function(i) {
        return [new Date(i.dt).getTime(), i[wq]];
      });
    });
  };
}]);

App.directive('chart', function() {
  return {
    restrict: 'C',
    template: '<div></div>',
    replace: true,
    scope: {plotData: '='},
    link: function(scope, elem, attrs) {
      scope.$watch('plotData', function(data) {
        if (!data) return;
        $.plot(elem, [data], {
          xaxis: {show: false, ticks: 4},
          //yaxis: {show: false},
          grid: {show: true},
          colors: ['#f00']
        });
      });
    }
  };
});
