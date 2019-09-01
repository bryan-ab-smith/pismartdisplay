var owKey = ''
var weatherCity = ''
var tempUnit = ''

var ouvKey = ''

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

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getUVLatLong)
    }

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
    setTimeout(getWeather, 1800000); // Every thirty minutes. The API services only allow so many free calls so I'm erring on the side of caution here.
}


function getUVLatLong(position) {
    uvURL = 'https://api.openweathermap.org/data/2.5/uvi?lat=' + position.coords.latitude + '&lon=-' + position.coords.longitude + '&appid=' + owKey;

    $.ajax({
        type: 'GET',
        dataType: 'json',
        beforeSend: function (request) {
            request.setRequestHeader('x-access-token', ouvKey);
        },
        url: 'https://api.openuv.io/api/v1/uv?lat=' + position.coords.latitude + '&lng=' + position.coords.longitude,
        success: function (response) {
            console.log(response.result.value)
            document.getElementById('uv').innerHTML = 'UV: ' + parseFloat(response.result.uv).toFixed(1) + ', max. ' + parseFloat(response.result.uv_max).toFixed(1);
        },
        error: function (response) {
            document.getElementById('uv').innerHTML = 'N/A';
        }
    });
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


$(document).ready(function () {
    $.getJSON("/static/config.json", function (data) {
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
            }
        });
    }).done(function () {
        getTime();

        getWeather();
    });
});