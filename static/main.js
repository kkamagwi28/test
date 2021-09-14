console.log('hello')

const ws = new WebSocket('ws://localhost:8828/ws/');
ws.onmessage = function(event){
    var data = JSON.parse(event.data);
    console.log(data);
    document.querySelector('#example').innerText = data.message;
}

