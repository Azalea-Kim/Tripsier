const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const forgetPasswordButton = document.getElementById('forget-password');
const sendButton = document.getElementById('send');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    console.log("clicked")
    container.classList.add("right-panel-active");
    container.classList.remove("forgetPassword");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");

});

forgetPasswordButton.addEventListener('click', () => {
    container.classList.add("forgetPassword");

});

sendButton.addEventListener('click', () => {
    container.classList.remove("forgetPassword");
});

var alertContent = document.getElementById("alert").innerHTML;
console.log(alertContent )
if(alertContent != null || alertContent.length != 0)
    {
        alert("content:"+alertContent);
        document.getElementById("alert").innerHTML =  '';
    }
function passwordCheck() {
    var mail = document.getElementById("email").value;
    var password = document.getElementById("passwd").value;
    if (mail === "" || password === "") {
        alert("Please enter the information")
    } else {
        alert("Login successfully!")
        window.location.href = '';
    }
}




function bindCaptchaBtnClick(event) {
    var time = 59;
    var _count = document.getElementById("varify"); //获取验证码按钮
    console.log(_count)
    var $this = $(this)
    var email = $("input[name='email']").val();
    if (!email) {
        alert("Please enter your email address first");
        return;
    }

    // Sending network requests through JS: Ajax
    $.ajax({
        url: "/sendCaptcha",
        method: "POST",
        data: {
            "email": email
        },
        success: function (res) {
            alert("Send Captcha Successfully")

            // 禁用按钮
            _count.disabled = true;
            // 开启定时器
            var timer = setInterval(function () {
                console.log("timer")
                // 判断剩余秒数
                if (time === 0) {
                    // 清除定时器和复原按钮
                    clearInterval(timer);
                    _count.disabled = false;
                    _count.innerHTML = 'Varify';
                } else {
                    _count.innerHTML = `${time}s`;
                    time--;
                }
            }, 1000);
            if (res['code'] === 200) {
                console.log(111);

            }
        }
    })
}
