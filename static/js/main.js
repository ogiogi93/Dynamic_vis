/**
 * Created by Ogiwara on 2016/12/01.
 */

var notificationTable = dc.dataTable("#dc-notification-table");
var plotTable = dc.dataTable("#dc-plot-table");
var timeRange = dc.lineChart('#dc-time-range');
var parseDatetime = d3.time.format("%Y-%m-%d %H:%M:%S").parse;
result.forEach(function (d) {
    d.interval_dc = parseDatetime(d.interval);
});

/* run data through crossfilter */
ndx = crossfilter(result);

/* Set dimension */
dimLocation = ndx.dimension(function (d) {
    return d.location_name;
});
dimTime = ndx.dimension(function (d) {
    return d.interval_dc;
});
/* Set group */
grpLocation = dimLocation.group().reduceSum(function (d) {
    return d.num_of_people;
});
grpTime = dimTime.group().reduceSum(function (d) {
    return d.num_of_people;
});
/* Time Range */
minTime = dimTime.bottom(1)[0].interval_dc;
maxTime = dimTime.top(1)[0].interval_dc;
render_plots()

function render_plots() {
    notificationTable
        .width(400)
        .height(400)
        .dimension(dimLocation)
        .group(function () {
            return "";
        })
        .size(4)
        .columns([
            function (d) {
                if (d.situation != 'Stable') {
                    return ('<div class="desc"><div class="thumb"><span class="badge bg-theme"><i class="fa fa-clock-o"></i></span></div><div class="details"><p><muted>' + d.interval + '</muted><br/>' + d.location_name + ' [' + d.situation + ']<br/>' + d.detail + '</p></div></div>');
                }
            }
        ])
        .sortBy(function (d) {
            return d.interval_dc;
        })
        .order(d3.descending);

    plotTable
        .width(400)
        .height(400)
        .dimension(dimLocation)
        .group(function () {
            return "";
        })
        .size(4)
        .columns([
            function (d) {
                if (d.situation != 'Stable') {
                    if (d.location_name == '食堂') {
                        return ('<div style="position: absolute; top: 50px; left: 70px;"><img src="/static/img/warninng.jpeg" style="width:80px; height: 25px;"></div>');
                    }
                }
            }
        ])
        .sortBy(function (d) {
            return d.interval_dc;
        })
        .order(d3.descending);

    timeRange
        .width(1200)
        .height(30)
        .dimension(dimTime)
        .margins({top: 0, right: 0, bottom: 20, left: -1})
        .group(grpTime)
        .x(d3.time.scale().domain([minTime, maxTime]));

    dc.renderAll();
}


