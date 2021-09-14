console.log('hello')

const ws = new WebSocket('ws://46.101.120.8:8828/ws/');
ws.onmessage = function(event){
    var data = JSON.parse(event.data);
    console.log(data);
    document.querySelector('#example').innerText = data.message;
}

