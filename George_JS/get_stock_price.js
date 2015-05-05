/**
 * Created by dustin on 5/4/15.
 */

function getPrice(ticker, div_id){
    var div = document.getElementById(div_id);
    var url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"+ticker+"%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json";

    $.getJSON(url, function (json)
    {
        var lastquote = json.query.results.quote.LastTradePriceOnly;
        var p = document.createElement('p');
        var t = document.createTextNode(lastquote);
        p.appendChild(t);
        div.appendChild(p);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    getPrice("TSLA", "quote_div");
});


