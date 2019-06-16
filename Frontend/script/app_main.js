let toestand;
const IP = 'http://169.254.10.1:5000';
const socket = io.connect(IP);

const enableSocketIO = function() {
  console.log('handle sockets');
  socket.emit('connect');
  socket.on('connected', function() {
    console.log('connectie geslaagd');
  });
};

const init = function() {
  console.log('DOM geladen');
  enableSocketIO();
};
console.log('test');
document.addEventListener('DOMContentLoaded', init);
