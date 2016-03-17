$(document).ready(function () {
    
    var f_username = false;
    var f_password = false;
    var f_confirm_password = false;
    var f_email = false;

    // 当用户名框失去焦点时，进行重复检测
    $(".username").blur(function () {
        $.get("/username_check/",{'username': $(this).val()}, function(result){
            $(".alert").html(result);
            if (result != "") {
                f_username = false;
            } else {
                f_username = true;
            }
        });
    });
    
    // 邮箱格式验证
    $(".email").blur(function () {
        var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
        if ($(this).val() != "" && !reg.test($(this).val())) {
            $(".alert").html("邮箱格式错误，请重新输入");
            f_email = false;
        } else {
            $(".alert").html("");
            if ($(this).val() != "") {
                f_email = true;
            } else {
                f_email = false;
            }
        }
    });
    
    // 确认密码验证
    $(".confirm_password").blur(function () {
        var password = $(".password").val();
        if ($(this).val() != "" && $(this).val() != password) {
            $(".alert").html("两次密码输入不一致，请检查");
            f_confirm_password = false;
        } else {
            $(".alert").html("");
            if ($(this).val() != "") {
                f_confirm_password = true;
            } else {
                f_confirm_password = false;
            }
        }
    });
    
    $(".password").blur(function () {
        if ($(this).val() == "") {
            f_password = false;
        } else {
            f_password = true;
        }
    });
    
    // 验证通过才能提交
    $(".submit_btn").click(function () {
        if (f_username && f_password && f_confirm_password && f_email) {
            return true;
        } else {
            if ($(".alert").html() == "") {
                $(".alert").html("请将信息填写完整后再点击提交注册按钮");
            }
            return false;
        }
    });
});