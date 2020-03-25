var jatimGetData = function(callback) {
    $.ajax({
        crossOrigin: true,
        url: 'http://covid19dev.jatimprov.go.id',
        dataType: 'json',
        success: function(data) {
          console.log(data)
        }
      });
}