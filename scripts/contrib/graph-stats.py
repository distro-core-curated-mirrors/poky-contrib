#! /usr/bin/env python3

import collections, datetime, os, sys
import gviz_api

this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_path, '..', 'lib'))
from buildstats import BuildStats, diff_buildstats, taskdiff_fields, BSVerDiff

# Tasks to hide from the graph
skiptasks = ('do_rm_work',)

path = sys.argv[1]
if os.path.isfile(path):
    stats = BuildStats.from_file_json(path)
elif os.path.isfile(os.path.join(path, 'build_stats')):
    stats = BuildStats.from_dir(path)
else:
    assert False

schema =  [("Row", "string"), ("Bar", "string"),
           ("Start", "datetime"), ("End", "datetime")]

Row = collections.namedtuple("Row", ["Row", "Bar", "Start", "End"])
data = []

for name,recipe in stats.items():
    for taskname, task in recipe.tasks.items():
        if taskname in skiptasks: continue

        start = datetime.datetime.fromtimestamp(task['start_time'])
        end = datetime.datetime.fromtimestamp(task['start_time']+task['elapsed_time'])
        row = Row(Row=name, Bar=taskname, Start=start, End=end)
        data.append(row)

page_template = """
<html>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript">
    google.charts.load('current', {'packages': ['timeline']});
    google.charts.setOnLoadCallback(loadChart);

    var data = {};
    var options = {
        avoidOverlappingGridLines: false,
        timeline: { groupByRowLabel: false },
    };

    function loadChart() {
        %(jscode)s
        data = jscode_data;
        drawChart();
    }
    function collapseToggled() {
        options.timeline.groupByRowLabel = event.target.checked;
        drawChart();
    }
    function drawChart() {
      var chart = new google.visualization.Timeline(document.getElementById('chart_div'));
      chart.draw(data, options);
    }
  </script>
  <body>
    <h1>buildstats timeline</h1>
    <input type="checkbox" id="collapse_check" onclick="collapseToggled()">
    <label for="collapse_check">Merge recipes into a single row</label>
    <div style="height: 800px" id="chart_div"></div>
  </body>
</html>
"""
data_table = gviz_api.DataTable(schema, sorted(data, key=lambda row: row.Start))
jscode = data_table.ToJSCode("jscode_data")
print(page_template % {"jscode": jscode})