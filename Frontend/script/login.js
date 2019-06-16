let toestand;

const afterselect = function(response) {
  if (response != false) {
    console.log(response);
    localStorage.setItem('allow', true);
    localStorage.setItem('userid', response);

    console.log(localStorage.getItem('userid'));
    console.log('toon succesbericht');
    window.location.replace('effecten.html');
  } else {
    console.log('Het passwoord en email komen niet overeen');
    document.querySelector('#js-error__message').innerHTML = `
		<p class="c-tekst c-tekst__rood">errormessage</p>
		`;
  }
};

const login = function() {
  const body = JSON.stringify({
    email: document.querySelector('#email').value,
    passwoord: document.querySelector('#passwoord').value
  });
  console.log(body);
  handleData(endpoint + 'login', afterselect, 'POST', body);
};

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
  });
};

const init = function() {
  console.log('DOM geladen');
  enableSocketIO();
  document.querySelector('.c-form').addEventListener('submit', login);
};
console.log('test');
document.addEventListener('DOMContentLoaded', init);
