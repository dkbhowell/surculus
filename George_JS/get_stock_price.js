/**
 * Created by dustin on 5/4/15.
 */

function getPrice(ticker, div_id){
    var div = document.getElementById(div_id);
    var url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22"+ticker+"%22)%0A%09%09&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json";

    $.getJSON(url, function (json)
    {
        console.log(json.query.results.quote);

        var lastquote = json.query.results.quote.LastTradePriceOnly;
        var change = json.query.results.quote.Change_PercentChange;
        var marketcap = json.query.results.quote.MarketCapitalization;;

        var priceText = document.createTextNode("Price (change): " + lastquote);
        var changeText = document.createTextNode("(" + change + ")");
        var capText = document.createTextNode("Market Cap: " + marketcap);
        var space = document.createTextNode('\u00A0'+'\u00A0'+'\u00A0');

        div.appendChild(priceText);
        div.appendChild(space)
        div.appendChild(changeText);
        div.appendChild(document.createElement('br'))
        div.appendChild(capText)
    });
}

document.addEventListener("DOMContentLoaded", function () {
    getPrice("TSLA", "quote_div");
});


