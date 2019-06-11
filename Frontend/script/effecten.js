let toestand;

const testevent = function() {
  console.log('er is op de zin geklikt');
  let testdata = {
    sfnummer: 42,
    ccvals: {
      5: 70,
      93: 60
    }
  };
  console.log(testdata);
  socket.emit('effect_toepassen', testdata);
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
const handle_events = function() {
  console.log('hande events');
  document.querySelector('#js-def_val').addEventListener('click', function() {
    console.log('def_val');

    let testdata = {
      sfnummer: 0,
      ccvals: {}
    };
    console.log(testdata);
    socket.emit('effect_toepassen', testdata);
  });
  document.querySelector('#js-effect1').addEventListener('click', function() {
    console.log('js-effect1');
    let testdata = {
      sfnummer: 24,
      ccvals: {
        93: 15
      }
    };
    console.log(testdata);
    socket.emit('effect_toepassen', testdata);
  });
  document.querySelector('#js-effect2').addEventListener('click', function() {
    console.log('js-effect2');
    let testdata = {
      sfnummer: 40,
      ccvals: {
        64: 50
      }
    };
    console.log(testdata);
    socket.emit('effect_toepassen', testdata);
  });
  document.querySelector('#js-effect3').addEventListener('click', function() {
    console.log('js-effect3');
    let testdata = {
      sfnummer: 56,
      ccvals: {
        91: 120
      }
    };
    console.log(testdata);
    socket.emit('effect_toepassen', testdata);
  });
};

const init = function() {
  console.log('DOM geladen');
  console.log(localStorage.getItem('userid'));

  enableSocketIO();
  handle_events();

  toestand = document.querySelector('.js-toestand');
};
console.log('test');
document.addEventListener('DOMContentLoaded', init);
