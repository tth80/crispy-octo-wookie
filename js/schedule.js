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

function Employee(id, name, preferred, workdays)
{
    this.id = id;
    this.name = name;
    this.preferred = preferred;
    this.workdays = workdays;

    this.locked_work = [];
    this.locked_holiday = [];

    this.lock_holiday = function(arr) {
        this.locked_holiday = this.locked_holiday.concat(arr);
    };

    this.lock_work = function(arr) {
        this.locked_work = this.locked_work.concat(arr);
    };

    this.is_locked_work = function(isodate) {
        return this.locked_work.indexOf(isodate) > -1;
    };

    this.is_locked_holiday = function(isodate) {
        return this.locked_holiday.indexOf(isodate) > -1;
    };

    this.is_preferred = function(dayOfWeek) {
        return this.preferred.indexOf(dayOfWeek) > -1;
    };
}

function Week(sunday, employees, budget)
{
    this.sunday = sunday;
    this.days = [];
    this.details = [];
    this.employees = employees;
    this.quota = [0, 0, 0, 0, 0, 0, 0];
    this.budget = budget;

    this.init = function() {
        for(var i=0;i<7;i++) {
            var add = i * 86400000;
            var iso = new Date(this.sunday.getTime() + add).toISOString().substr(0, 10);
            this.days.push(iso); // ordered index of days
            this.details[iso] = {};

            for(var ei=0,len=this.employees.length;ei<len;ei++) {
                var emp = this.employees[ei];
                
                var locked_work = emp.is_locked_work(iso);
                var locked_holiday = emp.is_locked_holiday(iso);

                var day_locked = locked_work || locked_holiday;
                var day_status = locked_work ? '10AM-8PM' : '-';
                var day_preferred = emp.is_preferred(i);

                this.quota[i] += locked_work || day_preferred ? 1 : 0;

                this.details[iso][emp.id] = {
                    status: day_status,
                    locked: day_locked,
                    preferred: day_preferred,
                };
            }
        }
    };

    this.init();
}

angular.module('SchedApp.controllers', [])
    .controller('pageController', function($scope, APIService) {
        $scope.title = "September 2015";

        // sunday..saturday
        $scope.budget = [2, 4, 4, 4, 4, 4, 5];

        $scope.employees = [
            new Employee(1, 'Jenna',        [1,2,3,4,5],        4),
            new Employee(2, 'Wendy',        [1,2,3,4,5],        4),
            new Employee(3, 'Samantha',     [1,2,4,5,6],        4),
            new Employee(4, 'Bartholomew',  [1,2,4,5,6],        5),
            new Employee(5, 'Jack',         [2,3,5,6],          4),
            new Employee(6, 'Daniel',       [0,1,2,3,4,5,6],    5),
        ];

        $scope.getEmployeeById = function(id) {
            for(var i=0, len=$scope.employees.length; i<len; i++) {
                if($scope.employees[i].id == id) return $scope.employees[i];
            }
            return null;
        };

        $scope.getEmployeeById(1).lock_holiday(['2015-09-01', '2015-09-02']);
        $scope.getEmployeeById(3).lock_work(['2015-09-01', '2015-09-25']);

        $scope.month = [
            new Week(new Date('2015-08-30T00:00:00+0000'), $scope.employees, $scope.budget),
            new Week(new Date('2015-09-06T00:00:00+0000'), $scope.employees, $scope.budget),
            new Week(new Date('2015-09-13T00:00:00+0000'), $scope.employees, $scope.budget),
            new Week(new Date('2015-09-20T00:00:00+0000'), $scope.employees, $scope.budget),
            new Week(new Date('2015-09-27T00:00:00+0000'), $scope.employees, $scope.budget),
        ];

    });

angular.module('SchedApp', [
    'SchedApp.services',
    'SchedApp.controllers'
]);
