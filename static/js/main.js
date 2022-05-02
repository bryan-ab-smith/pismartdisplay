function toggleAllLights(status) {
    $.ajax({ type: 'GET', url: '/allLights/' + status });
}

function toggleLight(status, name) {
    $.ajax({ type: 'GET', url: '/light/' + name + '/' + status });
}

function reboot() {
    console.log('Rebooting...');
    $.ajax({ type: 'GET', url: '/reboot' });
}
