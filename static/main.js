console.log('hello')

const ws = new WebSocket('ws://0.0.0.0:8828/ws/');
ws.onmessage = function(event){
    var data = JSON.parse(event.data);
    console.log(data);
    document.querySelector('#example').innerText = data.message;
}

