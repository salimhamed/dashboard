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
