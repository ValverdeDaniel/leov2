filterStocks = function () {
    var filter = $('#filter').val();
    var url = '/stocks/filter/' + filter;
    $.get(url, function (data) {
        $('#stock-list').html(data);
    });
}