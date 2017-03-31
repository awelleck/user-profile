/**
 * JS for Flask-SocketIO and chat
 * Andrew Welleck
 */
$(document).ready(function() {
  namespace = '/chat';
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  socket.on('connect', function() {
    socket.emit('success', {data: 'User connected!'});
  });

  socket.on('my_response', function(msg) {
    var current_user = '{{ current_user }}';
    var d = new Date();
    var month = d.getMonth();
    month = (month + 1) + '';
    if (month.length == 1) {
      month = '0' + month;
    }
    var day = d.getDate();
    day = day + '';
    if (day.length == 1) {
      day = '0' + day;
    }
    var year = d.getFullYear();
    year = year.toString().substr(2,2);
    var hours = d.getHours();
    hours = hours + '';
    if (hours.length == 1) {
      hours = '0' + hours;
    }
    var minutes = d.getMinutes();
    minutes = minutes + '';
    if (minutes.length == 1) {
      minutes = '0' + minutes;
    }
    match_timestamp = (month + '/' + day + '/' + year + ' ' + hours + ':' + minutes)
    $('#log').append($('<div/>').html('<div>' + current_user + ' | ' + msg.data + ' | ' + match_timestamp + '</div>').html());
    scrollToBottom();
  });

  $('form#emit').submit(function(event) {
    socket.emit('my_event', {data: $('#emit_data').val()});
    return false;
  });

  const msgs = document.getElementById('log');

  function getMessages() {
    shouldScroll = msgs.scrollTop + msgs.clientHeight === msgs.scrollHeight;
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
  var hours_offset = (offset / 60);
  console.log('Offset in hours: ' + hours_offset);
});
