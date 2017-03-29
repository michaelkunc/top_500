var decades = [{ name: 'fifties', decade: "50's", years: { '1950': 1, '1951': 2, '1952': 4 } },
    { name: 'sixties', decade: "60's", years: { '1962': 2, '1963': 5, '1966': 4, '1967': 1 } },
    { name: 'seventies', decade: "70's", years: { '1972': 4, '1974': 7, '1976': 4, '1978': 10 } }
]


function decade_year_chart() {

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
            data: all_data(decades)
        }],
        drilldown: {
            series: all_series(decades)
        }
    });
};


//utility functions
function add(a, b) {
    return a + b;
}


function all_data(decade_list) {
    var all_data = []
    decade_list.forEach(function(decade_object) {
        all_data.push({
            name: decade_object.decade,
            y: Object.values(decade_object.years).reduce(add, 0),
            drilldown: decade_object.decade
        })
    })
    return all_data
}

function drilldown_values(decade_object) {
    values = []
    for (var key in decade_object) {
        values.push([key, decade_object[key]])
    }
    return values

}

function all_series(decade_list) {
    var all_series = []
    decade_list.forEach(function(decade_object) {
        all_series.push({
            id: decade_object.decade,
            data: drilldown_values(decade_object.years)
        })
    })
    return all_series
}


decade_year_chart();