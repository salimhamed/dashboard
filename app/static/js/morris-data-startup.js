// 12 month spend line chart
var spend_by_month = Morris.Line({
    element: 'spend-by-month-chart',
    data: [{
        period: '2014-05',
        charges: 2666,
        revenue: 2647
    }, {
        period: '2014-06',
        charges: 4912,
        revenue: 2501
    }, {
        period: '2014-07',
        charges: 6767,
        revenue: 3689
    }, {
        period: '2014-08',
        charges: 6810,
        revenue: 2293
    }, {
        period: '2014-09',
        charges: 5670,
        revenue: 1881
    }, {
        period: '2014-10',
        charges: 4820,
        revenue: 1588
    }, {
        period: '2014-11',
        charges: 15073,
        revenue: 5175
    }, {
        period: '2014-12',
        charges: 10687,
        revenue: 2028
    }, {
        period: '2015-01',
        charges: 10687,
        revenue: 2028
    }, {
        period: '2015-02',
        charges: 10687,
        revenue: 2028
    }, {
        period: '2015-03',
        charges: 10687,
        revenue: 2028
    }, {
        period: '2015-04',
        charges: 8432,
        revenue: 1791
    }],
    xkey: 'period',
    ykeys: ['charges', 'revenue'],
    labels: ['Charges', 'Revenue'],
    pointSize: 3,
    hideHover: 'auto',
    preUnits: '$',
    resize: true
});


// optimization percentage
var optimization = Morris.Donut({
    element: 'optmization-donut-chart',
    data: [
        {label: "Optmized", value: 89.3},
        {label: "Unoptimized", value: 10.7}
    ],
    formatter: function (y, data) { return y + '%' },
    resize: true
});
optimization.select(0);
