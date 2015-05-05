/**
 * Created by dustin on 5/4/15.
 */
function toggleVisibility(element){
    if(element.style.display == 'block'){
        element.style.display = 'none'
    }else{
        element.style.display = 'block'
    }
}

function createButton(text, id){
    var btn = document.createElement("BUTTON");
    var t = document.createTextNode(text);     // Create a text node
    btn.appendChild(t);
    btn.id = id;
    btn.style.width="150px";
    return btn;
}

function createDiv(id){
    var div = document.createElement("div");
    div.id = id;
    return div;
}

function getZyngaTweets(targetDiv){
    var root_dir = "companies/Zynga/";
    var year = "2015";
    var month = "04";
    var day = "07";

    for(var j = 0; j < 19; j++){
        day = parseInt(day) + 1;
        var date = year + "-" + month + "-" + day;
        var dir = root_dir + date;

        $.ajax({
            url: dir + "/top_tweets_fixed",
            async: false,
            dataType: 'json',
            success: function (data) {
                var co_dates = zynga.dates;
                var json = data;

                var aJsonItem = json[0];
                var created = aJsonItem.created_at.substring(0, 10);
                var date = {dateStr:created, twitIds:[], totalRetweets:0};

                for(i = 0; i < json.length; i++){
                    var tweet_item = json[i];
                    var id = tweet_item.id_str;
                    var retweets = tweet_item.retweet_count
                    date.totalRetweets += retweets;
                    date.twitIds[date.twitIds.length] = id;
                }
                co_dates[co_dates.length] = date;
                addTweetsToUI(targetDiv, date);
            }
        });
    }
}

function addTweetsToUI(targetDiv, dateObj){
    var ids = dateObj.twitIds;
    var btn = createButton(dateObj.dateStr, dateObj.dateStr + "_btn");
    var div = createDiv(dateObj.dateStr + "_div");
    var tweet_div = createDiv(dateObj.dateStr + "_tweet_div");
    btn.addEventListener("click", function(){toggleVisibility(tweet_div);});
    div.appendChild(btn);
    for(var i = 0; i < ids.length; i++){
        var twitterId = ids[i];
        twttr.widgets.createTweet(
            twitterId, tweet_div,
            {
                conversation: 'all',    // or all
                cards: 'visible',  // or visible
                linkColor: '#cc0000', // default is blue
                theme: 'light'    // or dark
            })
            .then(function (el) {
                //el.contentDocument.querySelector(".footer").style.display = "none";
            });
    }

    tweet_div.style.display = 'none';
    div.appendChild(tweet_div);
    targetDiv.appendChild(div);
}

function getZyngaNews(divObj){
    $.ajax({
        url: 'ZyngaNews.json',
        async: false,
        dataType: 'json',
        success: function (data) {
            json = data;
            var new_div = document.createElement("div");
            new_div.id = "tesla_news_div";
            divObj.appendChild(new_div);

            for (i = 0; i < data.length; i++) {
                var news_item = data[i];
                var title = news_item.Title;
                var url = news_item.Url

                a = document.createElement("a");
                a.href = url;
                a.innerHTML = title;
                new_div.appendChild(a);
                var linebreak = document.createElement("br");
                new_div.appendChild(linebreak)
            }
        }
    });
}


document.addEventListener("DOMContentLoaded", function () {

    zynga = {name:"Zynga", dates:[], div:document.getElementById("zynga_div")};

    getZyngaTweets(zynga.div);
    getZyngaNews(zynga.div);
});
