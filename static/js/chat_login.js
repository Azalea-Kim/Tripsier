namespace = '/dcenter';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

function login() {
    //event name对应后端
    var username = $("#username").val()
    var room = $("#room").val()
    socket.emit('join',{'username':username,'room':room});
    console.log(username,room)
    window.location.href = "/a"
}