// define root api url
var api_url = 'http://' + $SCRIPT_ROOT + '/_api/';


// relationship summary bar chart
$.getJSON(
    api_url + 'firm_summary',
    function(chart_data) {

        var relationship_summary = Morris.Bar({
            element: 'firm-bar-chart',
            data: chart_data,
            xkey: 'type',
            ykeys: ['vc', 'ai', 'su'],
            labels: ['Venture Captial', 'Accelerator', 'Startup Org'],
            hideHover: 'auto',
            resize: true
        });

        relationship_summary.on('click', function(i, row) {
            console.log(i, row);
        });

});



// ai penetration donut
var ai_penetration = Morris.Donut({
    element: 'ai-penetration-donut',
    data: [
        {label: "On AWS", value: 72.3},
        {label: "Not On AWS", value: 28.4}
    ],
    formatter: function (y, data) { return y + '%' },
    resize: true
});
ai_penetration.select(0);
ai_penetration.on('click', function(i, row) {
    console.log(i, row);
});


// vc penetration donut
var vc_penetration = Morris.Donut({
    element: 'vc-penetration-donut',
    data: [
        {label: "On AWS", value: 42.3},
        {label: "Not On AWS", value: 57.7}
    ],
    formatter: function (y, data) { return y + '%' },
    resize: true
});
vc_penetration.select(0);
vc_penetration.on('click', function(i, row) {
    console.log(i, row);
});


// overall penetration donut
var overall_penetration = Morris.Donut({
    element: 'overall-penetration-donut',
    data: [
        {label: "On AWS", value: 60.5},
        {label: "Not On AWS", value: 39.5}
    ],
    formatter: function (y, data) { return y + '%' },
    resize: true
});
overall_penetration.select(0);
overall_penetration.on('click', function(i, row) {
    console.log(i, row);
});
