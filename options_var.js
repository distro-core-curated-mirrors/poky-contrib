var global_opt = {
    //title:'bitbake virtual/kernel #ubuntu12',
    vAxis: { format: 'HH:mm:ss', gridlines: {count:5}},
    curveType:'function',
    lineWidth: 3,
    series: [{'color': '#D3362D'}],
    intervals: { 'lineWidth':2, 'barWidth': 0.3 , 'color':'#F1CA3A'},
    interval: { 
        'i2': { 'style':'points', 'color':'grey', 'pointSize': 10,
        'lineWidth': 0, 'fillOpacity': 0.3 }
    },
    legend: 'none',
};


var url_chart1_virt_k = "getData/getData-ubuntu_bb-virtual-kernel.php"
var url_chart2_virt_k = "getData/getData-fedora_bb-virtual-kernel.php"
var url_chart1_bb_sato = "getData/getData-ubuntu_bb-sato.php"
var url_chart2_bb_sato = "getData/getData-fedora_bb-sato.php"
var url_chart1_bb_sato_rootfs = "getData/getData-ubuntu_bb-sato-rootfs.php"
var url_chart2_bb_sato_rootfs = "getData/getData-fedora_bb-sato-rootfs.php"
var url_chart1_bb_sato_rm_work = "getData/getData-ubuntu_bb-sato-rm_work.php"
var url_chart2_bb_sato_rm_work = "getData/getData-fedora_bb-sato-rm_work.php"
var url_chart1_bb_p = "getData/getData-ubuntu_bb-p.php"
var url_chart2_bb_p = "getData/getData-ubuntu_bb-p.php"
var url_chart1_bb_p_tmp = "getData/getData-ubuntu_bb-p-tmp.php"
var url_chart2_bb_p_tmp = "getData/getData-ubuntu_bb-p-tmp.php"
var url_chart1_bb_p_cache_tmp = "getData/getData-ubuntu_bb-p-cache-tmp.php"
var url_chart2_bb_p_cache_tmp = "getData/getData-fedora_bb-p-cache-tmp.php"