function sendJSONRequest(path, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', path, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                if (callback) {
                    callback(null, JSON.parse(xhr.responseText));
                }
            } else {
                if (callback) {
                    callback(new Error('Request failed: ' + xhr.status));
                }
            }
        }
    };
    xhr.send(JSON.stringify(data));
}