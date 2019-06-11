let toestand;

const afterinsertion = function(response) {
  if (response != false) {
    document.querySelector('#js-error__message').innerHTML = `
		<p class="c-tekst c-tekst__groen">Uw account is aangemaakt, u wordt herleid.</p>
		`;
    setTimeout(function() {
      window.location.replace('login.html');
    }, 3000);
  } else {
    //console.log('Account bestaat al!');
    document.querySelector('#js-error__message').innerHTML = `
		<p class="c-tekst c-tekst__rood">Er bestaat al een account met deze email</p>
		`;
  }
};

const registreer = function() {
  let email1 = document.querySelector('#email').value;
  let passwoord1 = document.querySelector('#passwoord1').value;
  let passwoord2 = document.querySelector('#passwoord2').value;

  console.log(email);
  if (passwoord1 == passwoord2) {
    //console.log('mag geregistreerd worden');

    // mocht er een foutcode staan mag deze weg
    document.querySelector('#js-error__message').innerHTML = '';

    const body = JSON.stringify({
      email: email1,
      passwoord: passwoord1
    });
    handleData(endpoint + 'register', afterinsertion, 'POST', body);
  } else {
    //console.log('Fout: wachtwoorden komen niet overeen');
    document.querySelector('#js-error__message').innerHTML = `
		<p class="c-tekst c-tekst__rood">De wachtwoorden komen niet overeen</p>
		`;
  }
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
  localStorage.clear();
  console.log('DOM geladen');
  enableSocketIO();

  document.querySelector('.c-form').addEventListener('submit', registreer);
};
document.addEventListener('DOMContentLoaded', init);
