/* ################## Configure block ################## */

// You have to replace the url below with an openweather appropriate URL (with city and API key): https://openweathermap.org/api
var weatherURL = ''

// You have to replace this with one of the supported cities by ARPANSA: https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring/ultraviolet-radation-data-information
// This is Australia only at the moment. I'll find a more international source.
var uvCity = ''

/* ################## End configure block ################## */

function getTime() {
    var time = new Date();

    var secs;
    var min;
    var hrs;

    if (time.getSeconds().toString().length < 2) {
        secs = '0' + time.getSeconds().toString()
    } else {
        secs = time.getSeconds().toString()
    }

    if (time.getMinutes().toString().length < 2) {
        min = '0' + time.getMinutes().toString()
    } else {
        min = time.getMinutes().toString()
    }

    if (time.getHours().toString().length < 2) {
        hrs = '0' + time.getHours().toString()
    } else {
        hrs = time.getHours().toString()
    }

    var curTime = hrs + ':' + min + ':' + secs;
    document.getElementById('time').innerHTML = curTime;
    setTimeout(getTime, 500);
}

function getWeather() {
    $.ajax({
        type: 'GET',
        url: weatherURL,
        datatype: 'json',
        success: function(json) {
            temp = Math.round(json.main.temp);
            conds = json.weather[0].main;
            
            document.getElementById('weather').innerHTML = temp + '&deg; (' + conds + ')';
        }
    });

    $.ajax({
        type: 'GET',
        url: 'https://uvdata.arpansa.gov.au/xml/uvvalues.xml',
        dataType: 'xml',
        success: function (xml) {
            $(xml).find('location').each(function () {
                if ($(this).attr('id') == uvCity) {
                    document.getElementById('uv').innerHTML = 'UV: ' + $(this).find('index').text();
                }
            })
        }
    });

    var time = new Date();

    var secs;
    var min;
    var hrs;

    if (time.getSeconds().toString().length < 2) {
        secs = '0' + time.getSeconds().toString()
    } else {
        secs = time.getSeconds().toString()
    }

    if (time.getMinutes().toString().length < 2) {
        min = '0' + time.getMinutes().toString()
    } else {
        min = time.getMinutes().toString()
    }

    if (time.getHours().toString().length < 2) {
        hrs = '0' + time.getHours().toString()
    } else {
        hrs = time.getHours().toString()
    }

    var curTime = hrs + ':' + min + ':' + secs;

    document.getElementById('weatherUpdateDate').innerHTML = 'Last update: ' + curTime;
    setTimeout(getWeather, 300000); // Five minutes
}

function toggleLight(status, name) {
    $.ajax({type: 'GET', url: '/light/' + status + '/' + name});
}

function toggleAllLights(status) {
    $.ajax({type: 'GET', url: '/allLights/' + status});
}


$(document).ready(function() {
    getTime();
   
    getWeather();
})