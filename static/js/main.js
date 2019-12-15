var owKey = ''
var weatherCity = ''
var tempUnit = ''

var ouvKey = ''

var lat = ''
var lng = ''

var hereAPI_key = ''

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

    var curDate = time.getDate() + '/' + time.getMonth() + '/' + time.getFullYear();
    document.getElementById('date').innerHTML = curDate;

    setTimeout(getTime, 500);
}

function getWeather() {
    weatherURL = 'https://api.openweathermap.org/data/2.5/weather?q=' + weatherCity + '&units=' + tempUnit + '&appid=' + owKey

    $.ajax({
        type: 'GET',
        url: weatherURL,
        datatype: 'json',
        success: function (json) {
            temp = Math.round(json.main.temp);
            conds = json.weather[0].main;
            document.getElementById('weather').innerHTML = temp + '&deg; (' + conds + ')';
        }
    });

    /*if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getUVLatLong, posError, {
            timeout: 30000,
            enableHighAccuracy: true
        })
    }*/

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
    setTimeout(getWeather, 1800000); // Every thirty minutes. The API services only allow so many free calls so I'm erring on the side of caution here to ensure no limiting.
    setTimeout(getUVLatLong, 1800000);
}

/*function posError(err) {
    console.log(err.message)
}*/

function getUVLatLong() {
    // https://www.openuv.io/uvindex
    $.ajax({
        type: 'GET',
        dataType: 'json',
        beforeSend: function (request) {
            request.setRequestHeader('x-access-token', ouvKey);
        },
        url: 'https://api.openuv.io/api/v1/uv?lat=' + lat + '&lng=' + lng,
        success: function (response) {
            document.getElementById('uv').innerHTML = 'UV: ' + parseFloat(response.result.uv).toFixed(1) + ', max. ' + parseFloat(response.result.uv_max).toFixed(1);
        },
        error: function (response) {
            console.log(response)
            document.getElementById('uv').innerHTML = 'N/A';
        }
    });
}

function getCity() {
    var platform = new H.service.Platform({
        'apikey': hereAPI_key
    });

    // https://developer.here.com/api-explorer/rest/geocoder/reverse-geocode
    var geocoder = platform.getGeocodingService(),
        parameters = {
            prox: lat + ',' + lng,
            mode: 'retrieveAddresses',
            maxresults: '1',
            gen: '9'
        };

    geocoder.reverseGeocode(parameters,
        function (result) {
            document.getElementById('location').innerHTML = result.Response.View[0].Result[0].Location.Address.City;
        }, function (error) {
            document.getElementById('location').innerHTML = 'Error.';
        });
}

function getNews() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/news',
        success: function (response) {

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
            document.getElementById('newsTitle').innerHTML = 'Top Headlines (as of ' + curTime + ')';
            document.getElementById('news').innerHTML = response[0] + '<br \\>' + '<small>' + response[1] + '</small><p></p>' + response[2] + '<br \\>' + '<small>' + response[3] + '</small><p></p>' + response[4] + '<br \\>' + '<small>' + response[5] + '</small><p></p>';
            //document.getElementById('uv').innerHTML = 'UV: ' + parseFloat(response.result.uv).toFixed(1) + ', max. ' + parseFloat(response.result.uv_max).toFixed(1);
        },
        error: function (response) {
            console.log(response)
            document.getElementById('news').innerHTML = 'N/A';
        }
    });
    setTimeout(getNews, 1800000);
}


function toggleAllLights(status) {
    if (status == 'True') {
        $.ajax({ type: 'GET', url: '/allLights/True' });
    } else {
        $.ajax({ type: 'GET', url: '/allLights/False' });
    }
}

function toggleLight(status, name) {
    if (status == 'True') {
        $.ajax({ type: 'GET', url: '/light/True/' + name });
    } else {
        $.ajax({ type: 'GET', url: '/light/False/' + name });
    }
}

function toggleAllPlugs(status) {
    if (status == 'True') {
        $.ajax({ type: 'GET', url: '/allPlugs/True' });
    } else {
        $.ajax({ type: 'GET', url: '/allPlugs/False' });
    }
}

function togglePlug(status, name) {
    if (status == 'True') {
        $.ajax({ type: 'GET', url: '/plug/True/' + name });
    } else {
        $.ajax({ type: 'GET', url: '/plug/False/' + name });
    }
}

function reboot() {
    console.log('Rebooting...');
    $.ajax({ type: 'GET', url: '/reboot' });
}

$(document).ready(function () {
    // https://api.jquery.com/jQuery.getJSON/
    $.getJSON("../static/config.json", function (data) {
        $.each(data, function (key, val) {
            switch (key) {
                case 'owAPI_key':
                    owKey = val;
                    break;
                case 'ow_loc':
                    weatherCity = val;
                    break;
                case 'ow_units':
                    tempUnit = val;
                    break;
                case 'ouvAPI_key':
                    ouvKey = val;
                    break;
                case 'lat':
                    lat = val;
                    break;
                case 'lng':
                    lng = val;
                    break;
                case 'hereAPI_key':
                    hereAPI_key = val;
                    break;
            }
        });
    }).done(function () {
        getTime();

        getWeather();

        getUVLatLong();

        //getCity();

        getNews();
    });
});