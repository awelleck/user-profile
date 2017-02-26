/**
 * JS for Flask-SocketIO and chat
 * Andrew Welleck
 */
$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  var offset = new Date().getTimezoneOffset();
  var second = '{{ second }}';
  console.log('Offset in minutes: ' + offset);
  var hours = offset / 60
  console.log('Offest in hours: ' + hours)

  socket.on('connect', function() {
    socket.send('User has connected!');
  });

  socket.on('message', function(msg) {
    $("#messages").append('<li>' + msg + '</li>');
    console.log('Received message!');
  });

  $('#submit').on('click', function() {
    socket.send($('#input').val());
    $('#input').val('');
  });
});
