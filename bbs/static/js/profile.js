$(function () {
    bind_wechat()
});


function bind_wechat() {
    $(".weixin-qrcode").on("mouseenter",function () {
       $(".del-wechat").removeClass("del-wechat-active");
    });

    $(".weixin-qrcode").on("mouseleave",function () {
       $(".del-wechat").addClass("del-wechat-active");
    });

    $(".infomation tr:eq(0) td:eq(1) input").on("click",function(){
        if (typeof($(this).attr("checked"))=="undefined") {
            $(this).attr("checked","checked").siblings().removeAttr("checked");
        }
    });


    $("#upload-wechat").on("change",function () {
        var id = $(".container-left .main-top").attr("data-id");
        var wechat = $("#upload-wechat")[0].files[0];
        var content = new FormData();
        content.append("id", id);
        content.append("wechat", wechat);
        $.ajax({
            url: '/bbs/setting/profile/bind_wechat',
            type: 'POST',
            data: content,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (data['status']) {
                    var domain = window.location.protocol + '//' + window.location.host;
                    if ($(".weixin-qrcode").has("img").length) {
                        $(".weixin-qrcode > img").attr("src", domain + "/" + data['url']);
                    } else {
                        _str_wechat = '<img src="' + domain + "/" + data['url'] + '"/>';
                        $(".weixin-qrcode").prepend(_str_wechat);
                    }
                }else {
                    alert("微信二维码上传失败");
                }
            }
        })
    });

    $(".setting-save").on("click", function () {
        var id = $(".login-user > .user-img").attr("data-id");
        var sex = $(".infomation tr:eq(0) td:eq(1) input:checked").val();
        var intro = $(".infomation tr:eq(1) td:eq(1) textarea").val();
        var web = $(".infomation tr:eq(2) td:eq(1) input").val();
        content = {
            "id":id,
            "sex":sex,
            "intro":intro,
            "web":web
        };
        $.ajax({
            url: '/bbs/setting/profile/save',
            type: 'POST',
            data: content,
            dataType: 'json',
            success: function (data) {
                if (!data['status']) {
                    alert("保存失败")
                }
            }
        })
    });
}