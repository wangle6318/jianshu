$(function(){
	replyNoticeComments();
	followOrCancle()
});

function replyNoticeComments(){
	$(".notice-reply").on("click",function(){
		var str_reply = '<div>' +
						'<form class="new-comment">' + 
							'<textarea placeholder="写下你的评论..."></textarea>' +
							'<div class="write-function-block">' +
								'<div class="hint">Ctrl+Enter 发表</div>' +
								'<a class="btn btn-send">发送</a>' +
								'<a class="cancel">取消</a>' +
							'</div>' +
						'</form>' +
					'</div>';
		if ($(this).parent().next().length == 0){
			$(this).parent().after(str_reply);
		}
	});
	
	$(".comment-list > li").on("click","form > div > .cancel",function(){
		$(this).parent().parent().parent().remove();	
	});
	
	$(".comment-list > li").on("click","form > div > .btn-send", function(){
		console.log("回复");
	});
}



function followOrCancle(){
	//关注
	$(".follow-list > li").on("click",".follow",function(){
		var followed_id=$(this).siblings("a").attr("href").split("=")[1];
		var content = {
			"followed_id": followed_id
		};
		var current = $(this);
		$.ajax({
			url:'/notice/follow_notice_list/set_following',
			type:'POST',
			dataType:'json',
			data:content,
			success:function (data) {
				if(data['status']){
					$(current).attr("class","btn btn-default follow-cancel");
					$(current).children("i").attr("class","iconfont icon-true2");
					$(current).children("span").text("已关注");
					return false;
				}else {
					alert("关注失败，请重试")
				}
			}
		});
	});
	//取消过程
	$(".follow-list > li").on("mousemove",".follow-cancel",function(){
		$(this).children("i").attr("class","iconfont icon-baseline-close-px");
		$(this).children("span").text("取消关注");
		return false;
	});
	
	$(".follow-list > li").on("mouseout",".follow-cancel", function(){
		$(this).children("i").attr("class","iconfont icon-true2");
		$(this).children("span").text("已关注");
		return false;
	});
	//取消关注
	$(".follow-list > li").on("click",".follow-cancel", function(){
		var followed_id=$(this).siblings("a").attr("href").split("=")[1];
		var content = {
			"followed_id": followed_id
		};
		var current = $(this);
		$.ajax({
			url:'/notice/follow_notice_list/cancel_following',
			type:'POST',
			dataType:'json',
			data:content,
			success:function (data) {
				if(data['status']){
					$(current).attr("class","btn btn-success follow");
					$(current).children("i").attr("class","iconfont icon-add1");
					$(current).children("span").text("关注");
					return false;
				}else {
					alert("取消关注失败，请重试")
				}
			}
		});

		// $(this).attr("class","btn btn-success follow");
		// $(this).children("i").attr("class","iconfont icon-add1");
		// $(this).children("span").text("关注");
		// return false;
	})
}




