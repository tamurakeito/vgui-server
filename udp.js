const dgram = require('dgram');

const PORT_A = 3002;
const HOST_A ='127.0.0.1';

const PORT_B = 3003;
const HOST_B ='127.0.0.1';

const socket = dgram.createSocket('udp4');

var count = 0;

setInterval(() => {
    count++;
    const data = Buffer.from(String(count));
    socket.send(data, 0, data.length, PORT_A, HOST_A, (err, bytes) => {
        if (err) throw err;
    });
}, 500);


socket.on('message', (message, remote) => {
    console.log(remote.address + ':' + remote.port +' - ' + message);
});

socket.bind(PORT_B, HOST_B);
