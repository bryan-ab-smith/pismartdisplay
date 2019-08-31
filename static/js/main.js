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
    // You have to replace the url below with an openweather appropriate URL (with city and API key): https://openweathermap.org/api
    $.ajax({
        type: 'GET',
        url: '',
        datatype: 'json',
        success: function (json) {
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
                // You have to replace this with one of the supported cities by ARPANSA: https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring/ultraviolet-radation-data-information
                if ($(this).attr('id') == '') {
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

function toggleBedroomLight(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/bedroomLightOn' });
    } else {
        $.ajax({ type: 'GET', url: '/bedroomLightOff' });
    }
}

function toggleDeskLampLight(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/deskLampLightOn' });
    } else {
        $.ajax({ type: 'GET', url: '/deskLampLightOff' });
    }
}

function toggleFrontHallLight(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/frontHallLightOn' });
    } else {
        $.ajax({ type: 'GET', url: '/frontHallLightOff' });
    }
}

function toggleAllLights(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/allLightsOn' });
    } else {
        $.ajax({ type: 'GET', url: '/allLightsOff' });
    }
}



function toggleFanSwitch(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/fanSwitchOn' });
    } else {
        $.ajax({ type: 'GET', url: '/fanSwitchOff' });
    }
}

function toggleDehumidSwitch(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/dehumidSwitchOn' });
    } else {
        $.ajax({ type: 'GET', url: '/dehumidSwitchOff' });
    }
}

function toggleAllSwitches(status) {
    if (status == 'on') {
        $.ajax({ type: 'GET', url: '/allSwitchesOn' });
    } else {
        $.ajax({ type: 'GET', url: '/allSwitchesOff' });
    }
}


$(document).ready(function () {
    getTime();

    getWeather();
})