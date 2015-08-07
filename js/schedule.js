angular.module('SchedApp.services', [])
    .factory('APIService', function($http) {
        var API = {};

        API.fetch = function() {
            return $http({
                method: 'JSONP', 
                url: '/page.html?callback=JSON_CALLBACK'
            });
        };

        return API;
    });

angular.module('SchedApp.controllers', [])
    .controller('pageController', function($scope, APIService) {
        $scope.employees = [
            {id:1, name:'Jenna',          preferred:[1,2,3,4,5],        req_per_week:5}, 
            {id:2, name:'Wendy',          preferred:[1,2,4,5,6],        req_per_week:4}, 
            {id:3, name:'Syn',            preferred:[1,2,4,5,6],        req_per_week:5},
            {id:4, name:'Bartholomew',    preferred:[2,3,5,6],          req_per_week:4},
            {id:5, name:'Johnson',        preferred:[1,2,3,4,5,6,7],    req_per_week:5}
        ];

        $scope.constraints = {
            1: {must_away: ['2015-09-01', '2015-09-02'], must_work: []},
            3: {must_away: [], must_work: ['2015-09-01']},
        };

        $scope.createWeek = function(sunday, template) {
            var container = {days:[], details:[]};

            container.days = [];
            for(var i=0;i<7;i++) {
                var add = i * 86400000;
                var iso = new Date(sunday.getTime() + add).toISOString().substr(0, 10);
                container.days.push(iso); // ordered index of days
                container.details[iso] = {};

                $scope.employees.forEach(function(emp, idx) {
                    var cs = $scope.constraints[emp.id] || {must_away:[], must_work:[]};
                    var must_away = cs.must_away.indexOf(iso) > -1;
                    var must_work = cs.must_work.indexOf(iso) > -1;

                    var day_locked = must_away || must_work;
                    var day_status = must_work ? '10AM-8PM' : '-';
                    var day_preferred = emp.preferred.indexOf(i) > -1;

                    container.details[iso][emp.id] = {
                        status: day_status,
                        locked: day_locked,
                        preferred: day_preferred,
                    };
                });
            }

            return container;
        };

        $scope.month = [
            $scope.createWeek(new Date('2015-08-30T00:00:00+0000')),
            $scope.createWeek(new Date('2015-09-06T00:00:00+0000')),
            $scope.createWeek(new Date('2015-09-13T00:00:00+0000')),
            $scope.createWeek(new Date('2015-09-20T00:00:00+0000')),
            $scope.createWeek(new Date('2015-09-27T00:00:00+0000')),
        ];

    });

angular.module('SchedApp', [
    'SchedApp.services',
    'SchedApp.controllers'
]);
