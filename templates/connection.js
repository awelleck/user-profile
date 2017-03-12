/**
 * JS for Flask-SocketIO and chat
 * Andrew Welleck
 */
$(document).ready(function() {
  namespace = '/chat';
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
  console.log(socket);

  socket.on('connect', function(){
    socket.emit('success', {data: 'User connected!'});
  });

  socket.on('my_response', function(msg) {
    var current_user = "{{ current_user }}";
    $('#log').append($('<div/>').html('<div>' + current_user + " | " + msg.data + '</div>').html());
  });

  $('form#emit').submit(function(event){
    socket.emit('my_event', {data: $('#emit_data').val()});
    return false;
  });

  var offset = new Date().getTimezoneOffset();
  console.log('Offset in minutes: ' + offset);
  var hours = (offset / 60);
  console.log('Offset in hours: ' + hours);
});
