const IP = 'http://192.168.0.117:5000';
const socket = io.connect(IP);
let testknop;

let endpoint = IP + '/api/v1/';

const logincontrol = function() {
  console.log(localStorage);
  if (localStorage.getItem('allow') == 'true') {
    console.log('ze geschiedenis zien');
    document.querySelector('.c-nav').innerHTML = `
        <nav class="c-nav">
            <ul class="o-list c-nav__list">
                <li><a class="c-nav__link" href="geschiedenis.html">Geschiedenis</a></li>
                <li><a class="c-nav__link" href="effecten.html">Effecten</a></li>
                <li><a class="c-nav__link" id="js-logout" href="">logout</a></li>
            </ul>
        </nav>
        `;
    document.querySelector('#js-logout').addEventListener('click', function() {
      localStorage.clear();
      socket.emit('logout');
    });
  }
};

document.addEventListener('DOMContentLoaded', logincontrol);
