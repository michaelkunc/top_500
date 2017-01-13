

var fifties = {decade: "50's", years: {'1950': 1,'1951': 2, '1952': 4}}

function chart() {

    // Create the chart
    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Albums by Decade/Year'
        },
        xAxis: {
            type: 'category'
        },

        legend: {
            enabled: false
        },

        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true
                }
            }
        },

        series: [{
            name: 'Decade',
            colorByPoint: true,
            data: [{
                name: fifties.decade,
                y: Object.values(fifties.years).reduce(add,0),
                drilldown: fifties.decade
            }
            // , {
            //     name: 'Fruits',
            //     y: 2,
            //     drilldown: 'fruits'
            // }, {
            //     name: 'Cars',
            //     y: 4,
            //     drilldown: 'cars'
            // }
            ]
        }],
        drilldown: {
            series: [{
                id: fifties.decade,
                data: drilldown(fifties.years)
            }, {
                id: 'fruits',
                data: [
                    ['Apples', 4],
                    ['Oranges', 2]
                ]
            }, {
                id: 'cars',
                data: [
                    ['Toyota', 4],
                    ['Opel', 2],
                    ['Volkswagen', 2]
                ]
            }]
        }
    });
};


//utility functions
function add(a,b){
    return a + b;
}

function drilldown(decade_object){
    values = []
    for(var key in decade_object){
        values.push([key, decade_object[key]])
    }
    return values

}





var list = [1,2,3,4,5,6]

chart();