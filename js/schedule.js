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
        $scope.days = [];
        $scope.constraints = {
            1: {must_away: ['2015-09-01', '2015-09-02'], must_work: []},
        };

        $scope.createWeek = function(sunday) {
            $scope.days = [];
            for(var i=0;i<7;i++) {
                $scope.days.push(new Date(sunday.getTime() + i * 86400000));
            }
        };

        $scope.createMonth = function(year, month) {
            var fd = new Date(year, month-1);
            console.log(year, month, 1);
            while(fd.getDay() != 0) fd = new Date(fd.setSeconds(fd.getSeconds()-86400));

            $scope.date_first = new Date(fd.getTime());
            console.log('First day: ', $scope.date_first);

            $scope.days = [];
            var done = false;
            var cur = new Date(fd.getTime());
            while(!done) {
                var nd = new Date(cur.getTime());

                $scope.days.push(nd);

                done = cur.getMonth() > month && cur.getDay() == 6;
                cur = new Date(cur.setSeconds(cur.getSeconds() + 86400));
                if(done) {
                    $scope.date_last = new Date(nd.getTime());
                }
            }
            console.log('Last day: ', $scope.date_last);
        };

        $scope.getDay = function(emp, day) {
            var isoday = day.toISOString().substr(0, 10);
            var c = $scope.constraints[emp.id] || {must_work:[], must_away:[]};
            if(c && c.must_work.indexOf(isoday) != -1) {
                return "must work";
            }
            if(c && c.must_away.indexOf(isoday) != -1) {
                return "must away";
            }
            return "off";
        };

        $scope.fillPreferred = function() {
            var day = $scope.date_first;
            while(day <= $scope.date_last) {
                day = day.setSeconds(day.getSeconds() + 86400000);
                for(var i=0,len=$scope.employees.length;i<len;i++) {
                }
            }
        }

        $scope.createWeek(new Date(2015, 7, 30));
        //$scope.createMonth(2015, 9);
        //$scope.fillPreferred();

        console.log($scope.days);
    });

angular.module('SchedApp', [
    'SchedApp.services',
    'SchedApp.controllers'
]);
