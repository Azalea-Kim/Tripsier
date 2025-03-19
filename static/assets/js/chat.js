var namespace = '/dcenter';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
var room_id

function getTime(){
    var myDate = new Date;
        var hour = myDate.getHours()
        var minute = myDate.getMinutes()

        if(parseInt(minute)<10){
            minute = "0" + minute
        }

        var str_time = hour.toString() + ":" + minute.toString()
        var pm_or_ar


        if(hour <= 12 && hour >= 0){
            pm_or_ar = "PM"
        }else{
            pm_or_ar = "AM"
        }
        return str_time+" "+pm_or_ar
}

$(document).ready(function () {
    namespace = '/dcenter';
    //event name对应后端

    socket.on('get_room',function (res){
        room_id = res.room
        console.log(room_id)
    })

    socket.on('private_message', function (res) {
        var message = res.data;
        var user_name = res.user
        var time_value = getTime()

        if (message) {
            $("#t").append("<li class=\"d-flex message\">\n" +
                "\n" +
                "<div class=\"mr-lg-3 me-2\">\n" +
                "<img class=\"avatar sm rounded-circle\" src=\"../static/assets/images/xs/avatar5.jpg\" alt=\"avatar\">\n" +
                "</div>\n" +
                "\n" +
                "<div class=\"message-body\">\n" +
                `<span class=\"date-time text-muted\">${user_name}, ${time_value}</span>\n` +
                "<div class=\"message-row d-flex align-items-center\">\n" +
                "\n" +
                "<div class=\"message-content p-3\">\n" +
                message +
                "</div>\n" +
                "\n" +
                "</div>\n" +
                "</div>\n" +
                "</li>");
            //改变文本的地方,接收消息
            //反单引号` `可以用${var}插入字符串内部变量
        }
    });
});



function sendMessage(){
    var message = $("#message_input").val()
    socket.emit("private_message",{'data':message,'room':room_id})
    var time_value = getTime()

    $("#t").append("<li class=\"d-flex message right\">\n" +
        "<div class=\"message-body\">\n" +
        '<span class=\"date-time text-muted\">'+`${time_value} `+'<i class=\"zmdi zmdi-check-all text-primary\"></i></span>\n' +
        "<div class=\"message-row d-flex align-items-center justify-content-end\">\n" +
        "\n" +
        "<div class=\"message-content border p-3\">\n" + message +
        "</div>\n" +
        "</div>\n" +
        "</div>\n" +
        "</li>");
}