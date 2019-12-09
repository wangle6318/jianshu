$(function(){
	
	trigleMenuBorder();
	cancleFollow();
	editorInfo();
});


function trigleMenuBorder(){
	var current = $(".trigger-menu > li");
	
	current.on("click",function(){
		$(this).addClass("active").siblings().removeClass("active")
	});
	
	current.on("mouseenter",function(){
		$(this).addClass("active")
	});
	
	current.on("mouseleave",function(){
		if ($(this).siblings().hasClass("active")) {
			$(this).removeClass("active")
		}
	});
}

function cancleFollow(){
	
	var cancle = $(".info .btn-default");
	cancle.on("mousemove",function(){
		$(this).text("取消关注")
	});
	
	cancle.on("mouseout",function(){
		$(this).text("已关注")
	});
}

function editorInfo(){
	var editor = $(".function-btn");
	var form = $(".profile-edit");
	var txt = $(".profile-edit textarea");
	var cancle = $(".profile-edit a");
	var save = $(".profile-edit .btn-hollow");
	var info = $(".description");
	
	editor.on("click",function(){
		form.css({
			"display":"block"
		});
		info.css({
			"display":"none"
		});
		txt.text($.trim(info.text()))
	});
	
	cancle.on("click",function(){
		form.css({
			"display":"none"
		});
		
		info.css({
			"display":"block"
		})
	});
	
	save.on("click",function(e){
		var id = $(".login-user > .user-img").attr("data-id");
		var intro = $(".profile-edit textarea").val();
		content = {
			"id": id,
			"intro": intro
		};
		$.ajax({
			url: '/bbs/main_page/save_intro',
			type: 'POST',
			data: content,
			dataType: 'json',
			success: function (data) {
				if (data['status']) {
					form.css({
						"display":"none"
					});

					info.css({
						"display":"block"
					});
					$(".description .js-intro").text(intro);
				}
			}
		});
		e.preventDefault();
	});
}
