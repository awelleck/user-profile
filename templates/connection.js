$(document).ready(function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	var offset = new Date().getTimezoneOffset();
	console.log(offset);

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
