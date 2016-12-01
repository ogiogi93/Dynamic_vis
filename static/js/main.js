/**
 * Created by Ogiwara on 2016/12/01.
 */

var notificationTable = dc.dataTable("#dc-notification-table");
var timeRange = dc.lineChart('#dc-time-range');

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

    timeRange
        .width(1200)
        .height(30)
        .dimension(dimTime)
        .margins({top: 0, right: 0, bottom: 20, left: -1})
        .group(grpTime)
        .x(d3.time.scale().domain([minTime, maxTime]));

    dc.renderAll();
}


