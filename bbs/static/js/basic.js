$(function(){
	change_bind();
	window.onresize = function(){
		bind_info()
	};
	upload_head_img();
	bind_email();
	unbind_email();
	bind_phone();
	basic_save();
});


function bind_info(){
	
	var left = $(document).width() / 3;
	var top = ($(document).height() - 314) / 2;
//	console.log(left)
//	console.log(top)
	$(".modal-dialog").css({
		"left": left,
		"top": top
	})
}



function change_bind(){
	var domain = window.location.protocol + '//' + window.location.host;

	$(".cancle-bind").parent().on("mouseenter",function(){
		$(this).children("a").removeClass("cancle-bind")
	});
	
	$(".cancle-bind").parent().on("mouseleave",function(){
		$(this).children("a").addClass("cancle-bind")
	});
	
	$(".container").on("click",".close",function(){
		$(".container .modal-dialog").remove()
	});
	
	$("#bind-phone").on("click",function(){
		_str_phone = '<div class="modal-dialog">' +
						'<div class="modal-header">' +
							'<h4 class="modal-title">绑定手机</h4>' +
							'<button type="button" class="close"><img src="' + domain + '/static/img/close.svg"/></button>' +
						'</div>' +
						'<div class="modal-body">' +
							'<div class="tips">' +
								'根据国家法律要求，目前只支持国内手机号。绑定遇到问题？' +
							'</div>' +
							'<form class="mobile-reset-password">' +
								'<div class="input-prepend restyle">' +
									'<div class="overseas">' +
										'<input type="text" placeholder="手机号" />'+
									'</div>' +
									'<div class="input-prepend security-up-code">' +
										'<input type="text" placeholder="短信验证码" />' +
										'<a class="btn-in-resend">发送验证码</a>' +
									'</div>' +
									'<a class="sign-in-button">确认</a>' +
								'</div>' +
							'</form>' +
						'</div>' +
					'</div>';
		$(".container").append(_str_phone);
		bind_info();	
	});
	
	$("#bind-email").on("click",function(){
		_str_email = '<div class="modal-dialog">' +
						'<div class="modal-header">' +
							'<h4 class="modal-title">绑定邮箱</h4>' +
							'<button type="button" class="close"><img src="' + domain + '/static/img/close.svg"/></button>' +
						'</div>' +
						'<div class="modal-body">' +
							'<form class="email-reset-password">' +
								'<div class="input-prepend restyle">' +
									'<div class="overseas">' +
										'<input type="text" placeholder="请输入你的常用邮箱" />'+
									'</div>' +
									'<div class="input-prepend security-up-code">' +
										'<input type="text" placeholder="验证码" />' +
										'<a class="btn-in-resend">发送验证码</a>' +
									'</div>' +
									'<a class="sign-in-button">确认</a>' +
								'</div>' +
							'</form>' +
						'</div>' +
					'</div>';
		$(".container").append(_str_email);
		bind_info();	
	});
	
	$("#cancel-bind-email").on("click",function(){
		sure = confirm("确定要解绑邮箱吗?");
		if (sure){
			_email = $(this).siblings("div").text();
			_str_email = '<div class="modal-dialog">' +
							'<div class="modal-header">' +
								'<h4 class="modal-title">安全验证</h4>' +
								'<button type="button" class="close"><img src="' + domain + '/static/img/close.svg"/></button>' +
							'</div>' +
							'<div class="modal-body">' +
								'<div class="tips">' +
								'为了保证你的账号安全，请先验证身份，验证成功后进行下一步操作，验证码10分钟内有效' +
								'</div>' +
								'<div class="tips email-contact">' +
									'<h3>' +
										'<span>用邮箱</span>' + _email +
										'<span>验证</span>' +
									'</h3>' +
								'</div>' +
								'<form class="unbind_email">' +
									'<div class="input-prepend restyle">' +
									'<div class="input-prepend security-up-code">' +
										'<input type="text" placeholder="验证码" />' +
										'<a class="btn-in-resend">发送验证码</a>' +
									'</div>' +
										'<a class="sign-in-button">确认</a>' +
									'</div>' +
								'</form>' +
							'</div>' +
						'</div>';
			$(".container").append(_str_email);
			bind_info();
		}
	})
}

function upload_head_img() {
	$("#upload_head_img").on("change",function () {
		// console.log($("#upload_head_img")[0].files[0]);
		var content  = new FormData();
		content.append("id",$(".login-user > .user-img").attr("data-id"));
		content.append("head_img", $("#upload_head_img")[0].files[0]);
		$.ajax({
			url:'/bbs/setting/basic/head_img',
			type:'POST',
			dataType:'json',
			data:content,
			processData:false,  // 告诉jquery不转换数据
            contentType:false,
			success:function (data){
				if(data['status']){
					var domain = window.location.protocol + '//' + window.location.host;
					$("#head_img").attr("src", domain + "/" + data['url']);
					$(".login-user > .user-img > img").attr("src",domain + "/" + data['url']);
				}
			}
		})
	})
}

function bind_email() {
	$(".container").on("click",".modal-dialog .email-reset-password .btn-in-resend",function () {
		email = $(this).parent().siblings(".overseas").children("input").val();
		$(this).parent().siblings(".overseas").children("input").attr("readonly",true);
		if (myreg.test(email)) {
			// console.log(email);
			$(this).parent().siblings(".overseas").children("input").attr("readonly",true);
			var content = new FormData();
			content.append("id", $(".login-user > .user-img").attr("data-id"));
			content.append("email", email);
			$.ajax({
				url: '/bbs/setting/basic/bind_email_code',
				type: 'POST',
				dataType: 'json',
				data: content,
				processData:false,  // 告诉jquery不转换数据
            	contentType:false,
				success: function (data) {
					if (data['status']){
						var btn = $(".container .modal-dialog .email-reset-password .btn-in-resend");
						btn.attr("disabled",true).css("pointer-events","none");
						var interValobj;
						var count = 600;
						var curCount = count;
						btn.html(curCount + "s后重发");
						interValobj = window.setInterval(function(e){
							if (curCount) {
								curCount--;
								btn.html(curCount + "s后重发");
							} else{
								window.clearInterval(interValobj);
								$(".container .modal-dialog .email-reset-password .overseas input").attr("readonly", false);
								btn.html("发送验证码");
								btn.attr("disabled",false).css("pointer-events","auto");
							}
						},1000);
					} else {
						alert(data['message']);
					}
				}
			})
		} else {
			alert("您输入的邮箱格式不正确，请输入正确的邮箱")
		}
	});

	$(".container").on("click",".modal-dialog .email-reset-password .sign-in-button",function () {
		email = $(this).siblings(".overseas").children("input").val();
		code = $(this).siblings(".security-up-code").children("input").val();
		var content = new FormData();
		content.append("id", $(".login-user > .user-img").attr("data-id"));
		content.append("email", email);
		content.append("code", code);
		$.ajax({
			url: '/bbs/setting/basic/bind_email',
			type: 'POST',
			dataType: 'json',
			data: content,
			processData: false,  // 告诉jquery不转换数据
			contentType: false,
			success: function (data) {
				if (data['status']){
					$(".container .modal-dialog").remove();
					_str_email = 	'<td class="setted">' +
										'<div>' + email + '</div>' +
										'<a class="cancle-bind" id="cancel-bind-email">取消绑定</a>' +
									'</td>';
					block_email = $(".container-right .base tr:eq(2)");
					block_email.children("td:eq(1)").remove();
					block_email.append(_str_email);
				} else {
					alert(data['message']);
				}
			}
		})
	});
}

function unbind_email() {
	$(".container").on("click",".modal-dialog .unbind_email .btn-in-resend",function () {
		email = $("#cancel-bind-email").siblings("div").text();
		var content = new FormData();
		content.append("id", $(".login-user > .user-img").attr("data-id"));
		content.append("email", email);
		$.ajax({
			url: '/bbs/setting/basic/unbind_email_code',
			type: 'POST',
			dataType: 'json',
			data: content,
			processData: false,  // 告诉jquery不转换数据
			contentType: false,
			success: function (data) {
				if (data['status']){
					var btn = $(".container .modal-dialog .unbind_email .btn-in-resend");
					btn.attr("disabled",true).css("pointer-events","none");
					var interValobj;
					var count = 600;
					var curCount = count;
					btn.html(curCount + "s后重发");
					interValobj = window.setInterval(function(e){
						if (curCount) {
							curCount--;
							btn.html(curCount + "s后重发");
						} else{
							window.clearInterval(interValobj);
							btn.html("发送验证码");
							btn.attr("disabled",false).css("pointer-events","auto");
						}
					},1000);
				}
			}
		})
	});

	$(".container").on("click",".modal-dialog .unbind_email .sign-in-button",function () {
		email = $("#cancel-bind-email").siblings("div").text();
		code = $(this).siblings(".security-up-code").children("input").val();
		var content = new FormData();
		content.append("id", $(".login-user > .user-img").attr("data-id"));
		content.append("email", email);
		content.append("code", code);
		$.ajax({
			url:'/bbs/setting/basic/unbind_email',
			type: 'POST',
			dataType: 'json',
			data: content,
			processData: false,
			contentType: false,
			success: function (data) {
				if (data['status']){
					$(".container .modal-dialog").remove();
					_str_email = 	'<td class="setted">' +
										'<button class="btn btn-hollow" id="bind-email">点击绑定</button>' +
									'</td>';
					block_email = $(".container-right .base tr:eq(2)");
					block_email.children("td:eq(1)").remove();
					block_email.append(_str_email);
				} else {
					alert(data['message'])
				}
			}
		})
	})
}

function bind_phone() {
	$(".container").on("click",".modal-dialog .mobile-reset-password .btn-in-resend",function (){
		phone = $(this).parent().siblings(".overseas").children("input").val();
		myreg = /^1\d{10}$/;
		if (myreg.test(phone)){
			$(this).parent().siblings(".overseas").children("input").attr("readonly",true);
			var content = new FormData();
			content.append("id", $(".login-user > .user-img").attr("data-id"));
			content.append("phone", phone);
			$.ajax({
				url: '/bbs/setting/basic/bind_phone_code',
				type: 'POST',
				data: content,
				dataType: 'json',
				processData: false,
				contentType: false,
				success: function (data) {
					if (data['status']){
						alert(data['message']);
						// $(".container .modal-dialog").remove();
					}
				}
			})
		} else {
			alert("手机号码格式不正确")
		}
	});

	$(".container").on("click",".modal-dialog .mobile-reset-password .sign-in-button",function (){
		phone = $(this).parent().siblings(".overseas").children("input").val();
		code = $(this).siblings(".security-up-code").children("input").val();
		var content = new FormData();
		content.append("id", $(".login-user > .user-img").attr("data-id"));
		content.append("phone", phone);
		content.append("code", code);
		$.ajax({
			url: '/bbs/setting/basic/bind_phone',
			type: 'POST',
			data: content,
			dataType: 'json',
			processData: false,
			contentType: false,
			success: function (data) {
				if (data['status']){
					alert(data['message']);
					$(".container .modal-dialog").remove();
				}
			}
		})
	})
}

function basic_save() {
	$(".setting-save").on("click",function () {
		username = $(".base > tr:eq(1) > td:eq(1) > input").val();
		user_id = $(".login-user > .user-img").attr("data-id");
		var content = new FormData();
		content.append("id", user_id);
		content.append("username", username);
		$.ajax({
			url:'/bbs/setting/basic/save',
			type:'POST',
			dataType:'json',
			data:content,
			processData:false,
			contentType:false,
			success:function (data) {
				if (data['status']) {
					alert(data['message'])
				} else {
					alert(data['message'])
				}
			}
		})
	})
}