let toestand;
const IP = 'http://169.254.10.1:5000';
const socket = io.connect(IP);
const enableSocketIO = function() {
  console.log('handle sockets');
  socket.emit('connect');
  socket.on('connected', function() {
    console.log('connectie geslaagd');
  });
  socket.on('datatest', function(waarde) {
    console.log(waarde);
  });
  socket.on('toestand', function(waarde) {
    console.log(waarde);
    toestand.innerHTML = `${waarde} seconden`;
  });
};

const init = function() {
  console.log('DOM geladen');
  enableSocketIO();
  toestand = document.querySelector('.js-toestand');

  document.querySelector('.js-toestand').addEventListener('click', function() {
    console.log('Er is geklikt op de knop');
  });
};
console.log('test');
document.addEventListener('DOMContentLoaded', init);
