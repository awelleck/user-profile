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
    var offset = '{{ offset }}';
    var d = new Date();
    var month = d.getUTCMonth();
    month = (month + 1) + '';
    if (month.length == 1) {
      month = '0' + month;
    }
    var day = d.getUTCDate();
    day = day + '';
    if (day.length == 1) {
      day = '0' + day;
    }
    var year = d.getUTCFullYear();
    year = year.toString().substr(2,2);
    var hours = d.getUTCHours();
    if (hours - offset > 0) {
      hours = hours - offset
    } else {
      hours = ((24 + hours) - offset)
    }
    hours = hours + '';
    if (hours.length == 1) {
      hours = '0' + hours;
    }
    var minutes = d.getUTCMinutes();
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
});
