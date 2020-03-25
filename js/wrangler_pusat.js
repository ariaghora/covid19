var pusatGetData = function(callback) {
    $.get('https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?f=json&where=(Kasus_Posi%20%3C%3E%200)%20AND%20(Provinsi%20%3C%3E%20%27Indonesia%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Kasus_Posi%20desc&outSR=102100&resultOffset=0&resultRecordCount=34&cacheHint=true', function(res) { 
        var rawJson = res;
        var arrProvinsi = JSON.parse(rawJson).features;
        var result = [];
        var cnt = 1;
        for (const o of arrProvinsi) {
            var newObj = {
                no: cnt,
                nama: o.attributes.Provinsi,
                jml_kasus: o.attributes.Kasus_Posi,
                jml_sembuh: o.attributes.Kasus_Semb,
                jml_meninggal: o.attributes.Kasus_Meni,
                jml_odp: '-',
                jml_pdp: '-'
            }
            cnt++;
            result.push(newObj);
        }
        callback(result);
    })
}