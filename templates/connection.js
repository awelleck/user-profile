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
    scrollToBottom();
  });

  $('form#emit').submit(function(event){
    socket.emit('my_event', {data: $('#emit_data').val()});
    return false;
  });

  const msgs = document.getElementById('log');

  function getMessages() {
    shouldScroll = msgs.scrollTop + msgs.clientHeight === msgs.scrollHeight;
    console.log(shouldScroll);
    if (!shouldScroll) {
      scrollToBottom();
    }
  }

  function scrollToBottom() {
    msgs.scrollTop = msgs.scrollHeight;
  }

  scrollToBottom();
  getMessages();

  var offset = new Date().getTimezoneOffset();
  console.log('Offset in minutes: ' + offset);
  var hours = (offset / 60);
  console.log('Offset in hours: ' + hours);
});
