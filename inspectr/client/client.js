function RequestManager () {
    var self = this;
    this.requests = new Object();
    this.counter = 0;
    this.addRequest = function (data) {
        var id = self.counter;
        self.requests[self.counter.toString()] = data.request;
        self.counter++;
        return id;
    };
    this.getRequest = function (id) {
        return self.requests[id];
    };
}

function Client() {
    var self = this;
    this.url = "ws://" + location.host + "/ws";
    this.ws = new WebSocket(this.url);
    this.manager = new RequestManager();

    this.addEvent = function (event_data) {
        var rid = self.manager.addRequest(event_data);
        var el = document.getElementById('request-list');
        var li = document.createElement('li');
        li.setAttribute('class', 'list-group-item');
        li.setAttribute('rid', rid.toString());
        li.addEventListener('click', loadOnClick);
        li.appendChild(document.createTextNode('Request: ' + event_data.request.url));
        el.appendChild(li);
    };

    this.ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        console.log(data);
        if (data.event === "response_received" || data.event === "request_scheduled") {
            self.addEvent(data);
        }
    };
}

var client = new Client();

function loadOnClick(event){
    // disable current active element
    var active_items = document.getElementsByClassName('list-group-item active');
    if (active_items.length > 0) {
        var current = active_items[0];
        current.className = current.className.split(' ')[0];
    }

    // set clicked element as active
    this.className += ' active';
    var id = this.getAttribute('rid');

    // Embed the data related to the selected request in the textarea
    var request = client.manager.getRequest(id);
    var text_area = document.getElementById('code');
    text_area.value = JSON.stringify(request, null, 4);
}
$('document').ready(function () {
    $(function() {
        $('.col').matchHeight();
    });
});