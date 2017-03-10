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
    $('#log').append($('<div/>').html('<div>' + msg.data + '</div>').html());
  });

  $('form#emit').submit(function(event){
    socket.emit('my_event', {data: $('#emit_data').val()});
    return false;
  });
});
