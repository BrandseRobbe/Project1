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

const init = function() {
	console.log('DOM geladen');
	console.log(localStorage.getItem('userid'));

	enableSocketIO();

	toestand = document.querySelector('.js-toestand');

	testknop = document.querySelector('.testknop');
	testknop.addEventListener('click', function() {
		testevent();
	});
};
console.log('test');
document.addEventListener('DOMContentLoaded', init);
