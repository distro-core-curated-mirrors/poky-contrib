var global_opt = {
    title:'bitbake virtual/kernel #ubuntu12',
    vAxis: { format: 'HH:mm:ss', gridlines: {count:5}},
    curveType:'function',
    lineWidth: 4,
    series: [{'color': '#D3362D'}],
    intervals: { 'lineWidth':1, 'barWidth': 0.2 , 'color':'#F1CA3A'},
    interval: { 
        'i2': { 'style':'points', 'color':'grey', 'pointSize': 10,
        'lineWidth': 0, 'fillOpacity': 0.3 }
    },
    legend: 'none',
};