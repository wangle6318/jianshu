$(function(){
	commentEnter();
	authorOnly();
	thumbsup();
	// replyComment();
	// replyReplyComment();
	submit_comment();
	submit_reply_comment();
	goTop();
	markArticle();
	loveArticle();
	following_author();
});

function commentEnter(){
	var txt = $(".new-comment textarea");
	var cancle = $(".cancel-comment");
	var __cancle = $(".sub-comment-list .new-comment .cancel");
	txt.on("click",function(){
		$(this).siblings(".write-function-block").css({
			"display":"block"
		})
	});

	cancle.on("click",function(){
		$(this).parent().css({
			"display":"none"
		})
	});

	$(".normal-comment-list").on("click",".new-comment .cancel",function(){
		$(this).parentsUntil(".comment").filter(".sub-comment-list").children(".reply-form").css({
			"display":"none"
		})
	})
}

function authorOnly(){
	author = $(".author-only");
	author.on("click",function(){
		if (author.hasClass("active")) {
			author.removeClass("active")
		} else{
			author.addClass("active")
		}
	})
}

function thumbsup(){
	var thumbs = $(".tool-group .thumbsup");
	$(".normal-comment-list").on("click",".tool-group .thumbsup",function(){
		console.log($(this).parentsUntil("comment").filter(".comment-content").hasClass("comment-content"));
		let comment_id, is_reply;
		if($(this).parentsUntil("comment").filter(".comment-content").hasClass("comment-content")){
			comment_id = $(this).parentsUntil("comment").filter(".comment-content").parent(".comment").attr("data-cid");
			is_reply = false;
		}else {
			comment_id = $(this).parentsUntil(".sub-comment").filter(".tool-group").parent(".sub-comment").attr("data-cid");
			is_reply = true;
		};
		let content = {
		    "comment_id": comment_id,
            "is_reply": is_reply
        };
		let current = $(this);
		$.ajax({
            url:'/bbs/article/thumbs_up',
            type:'POST',
            dataType:'json',
            data:content,
            success:function (data) {
                switch (data['status']) {
                    case -1:
                        new_href = data['url'];
					    window.location.href = new_href;
					    break;
                    case 1:
                        oldsrc = current.find("img").attr("src");
                        newsrc = "";
                        if (oldsrc.indexOf("-a") == -1) {
                            newsrc = oldsrc.split("-")[0] +"-a.svg";
                        } else{
                            newsrc = oldsrc.split("-")[0] +"-b.svg";
                        }
                        current.find("img").attr("src",newsrc);
                }
            }
        });
	})
}

function submit_comment() {
	$(".submit-comment").on("click",function () {
		var article_id = $(".article > .title").attr("data-article");
		var comment = $(this).parent().siblings("textarea");
		var content = {
			"article_id":article_id,
			"text": comment.val()
		};
		$.ajax({
			url:"/bbs/article/submit_comment",
			type:'POST',
			dataType:'json',
			data:content,
			success:function (data) {
				switch (data['status']) {
                    case -1:
                        new_href = data['url'];
					    window.location.href = new_href;
					    break;
                    case 0:
                        alert("评论失败，请重试");
                        break;
                    case 1:
                        var domain = window.location.protocol + '//' + window.location.host;
                        var nc_str = '<div class="comment" data-cid="' + data['comment']['id'] + '">' +
                                        '<div class="comment-content">' +
                                            '<div class="author" data-uid="' + data['comment']['uid'] + '">' +
                                                '<div class="v-tooltip-container">' +
                                                    '<div class="v-tooltip-content">' +
                                                        '<a href="javascript:void(0);" class="avatar"><img src="' + domain +  '\\media\\' + String(data['comment']['head_img']) + '" alt="" /></a>' +
                                                    '</div>' +
                                                '</div>' +
                                                '<div class="info">' +
                                                    '<a href="javascript:void(0);" class="name">' + data['comment']['name'] + '</a>' +
                                                    '<div class="meta">' +
                                                        '<span>' + data['comment']['submit_time'] + '</span>' +
                                                    '</div>' +
                                                '</div>' +
                                            '</div>' +
                                            '<div class="comment-wrap">' +
                                                '<p>'+ data['comment']['text'] +'</p>' +
                                                '<div class="tool-group">' +
                                                    '<a href="javascript:void(0);" class="thumbsup">' +
                                                        '<img src="'+ domain + '/static/img/thumbsup-b.svg' + '"/>' +
                                                        '<span>赞</span>' +
                                                    '</a>' +
                                                    '<a href="javascript:void(0);" class="reply">' +
                                                        '<img src="' + domain + '/static/img/comment.svg' + '"/>' +
                                                        '<span>回复</span>' +
                                                    '</a>' +
                                                '</div>' +
                                            '</div>' +
                                        '</div>' +
                                        '<div class="sub-comment-list">' +
                                            '<div style="display: none;" class="reply-form">' +
                                                '<form class="new-comment">' +
                                                    '<textarea placeholder="写下你的评论..."></textarea>' +
                                                    '<div class="write-function-block">' +
                                                        '<a href="javascript:void(0);" class="btn btn-send submit-reply">发送</a>' +
                                                        '<a href="javascript:void(0);" class="cancel">取消</a>' +
                                                    '</div>' +
                                                '</form>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>';
                        let area = $(".normal-comment-list > div:first > div:first") ;
                        let r_area = $(".normal-comment-list .top-title");
                        area.after(nc_str);
                        r_area.siblings("div").remove();
                        $(comment).val("");
                        break;
                }
			}
		})
	})
}

function submit_reply_comment() {
    submit_reply();
    replyComment();
    replyReplyComment();
    let author_to_id,comment_id;

    function submit_reply() {
        $(".sub-comment-list .reply-form .btn-send").on("click",function () {
            let article_id = $(".article > .title").attr("data-article");
		    let text = $(this).parent().siblings("textarea");
		    let content = {
		        "article_id": article_id,
                "text":text.val(),
                "comment_id":comment_id,
                "author_to_id":author_to_id
            };
		    let current_area = $(this);
            $.ajax({
                url: '/bbs/article/submit_reply',
                type: 'POST',
                dataType: 'json',
                data: content,
                success:function (data) {
					switch (data['status']) {
						case -1:
							new_href = data['url'];
					    	window.location.href = new_href;
					    	break;
						case 0:
							alert("评论失败，请重试");
							break;
						case 1:
							var domain = window.location.protocol + '//' + window.location.host;
                        	var nc_str = '<div class="sub-comment" data-cid="' + data['reply']['id'] + '">' +
											'<p>' +
												'<span data-uid="' + data['reply']['uid'] + '">' + data['reply']['name'] +' <strong>回复</strong> ' + data['reply']['author_to'] + '</span>' +
												'<span>' + data['reply']['text'] + '</span>' +
											'</p>' +
											'<div class="tool-group">' +
												'<a href="javascript:void(0);" class="thumbsup">' +
													'<img src="'+ domain + '/static/img/thumbsup-b.svg' + '"/>' +
													'<span>赞</span>' +
												'</a>' +
												'<a href="javascript:void(0);" class="reply">' +
													'<img src="' + domain + '/static/img/comment.svg' + '"/>' +
													'<span>回复</span>' +
												'</a>' +
											'</div>' +
								           '</div>';
							var area = current_area.parentsUntil(".sub-comment-list").filter(".reply-form").before(nc_str);
							text.val("");
							current_area.parentsUntil(".sub-comment-list").filter(".reply-form").css({
								"display":"none"
							});
							break;
					}
                }
            })
        })
    }

    function replyComment(){
        $(".normal-comment-list").on("click",".comment-content .tool-group .reply",function(){
            $(this).parentsUntil(".comment").filter(".comment-content").siblings(".sub-comment-list").children(".reply-form").css({
                "display":"block"
            });
            author_to_id=$(this).parentsUntil(".comment-content").filter(".comment-wrap").siblings(".author").attr("data-uid");
            comment_id =$(this).parentsUntil(".comment").filter(".comment-content").parent(".comment").attr("data-cid");
        });
    }

    function replyReplyComment(){
        $(".normal-comment-list").on("click",".sub-comment-list .sub-comment .tool-group .reply-reply",function(){
            $(this).parentsUntil(".sub-comment-list").filter(".sub-comment").siblings(".reply-form").css({
                "display":"block"
            });
            author_to_id=$(this).parentsUntil(".sub-comment").filter(".tool-group").siblings("p").children("span:first").attr("data-uid");
            comment_id= $(this).parentsUntil(".comment").filter(".sub-comment-list").parent(".comment").attr("data-cid");
        });
    }
}

function goTop(){
	$(document).scroll(function(){	
		var top = $(document).scrollTop();
		var side_tool = $(".side-tool li:first-child");
		if (top > 400){
			side_tool.css({
				"display":"block"
			})
		} else{
			side_tool.css({
				"display":"none"
			})
		}		
	});
	
	var side_tool = $(".side-tool li:first-child");
	side_tool.on("click",function(){
            $('body,html').animate({scrollTop:0},300);	
	})
}

function markArticle(){
	var mark = $(".side-tool .mark");
	mark.on("click",function(){
		article_id = $(".article > .title").attr("data-article");
		content = {
			"article_id":article_id
		};
		$.ajax({
			url:'/bbs/collection',
			type:'POST',
			dataType:'json',
			data:content,
			success:function (data) {
				oldsrc = mark.find("img").attr("src");
				if (data['status']){
					newsrc = oldsrc.split(".")[0]+"-active.svg"
				} else {
					newsrc = oldsrc.split("-")[0]+".svg"
				}
				mark.find("img").attr("src",newsrc)
			}
		});
	})
}

function loveArticle(){
	var love = $(".side-tool .love");
	love.on("click",function(){
	    article_id = $(".article > .title").attr("data-article");
		content = {
			"article_id":article_id
		};
		$.ajax({
            url: '/bbs/love',
            type: 'POST',
            dataType: 'json',
            data: content,
            success: function (data) {
                oldsrc = love.find("img").attr("src");
                if (data['status']) {
                    newsrc = oldsrc.split(".")[0] + "-active.svg"
                } else {
                    newsrc = oldsrc.split("-")[0] + ".svg"
                }
                love.find("img").attr("src", newsrc)
            }
        })
	})
}

function following_author(){
	$(".info").on("mouseenter",".following",function(){
		$(this).text("取消关注")
	});

	$(".info").on("mouseleave",".following",function(){
		$(this).text("已关注")
	});

	$(".info").on("click",".follow",function(){
		var followed = $(".article > .author > .avatar").attr("href").split("=")[1];
		var content = {
			"followed":followed
		};
		$.ajax({
			url: "/bbs/set_following",
			type: "POST",
			data: content,
			dataType: "json",
			success: function (data) {
				if(data['status']){
					$(".follow").removeClass("follow").removeClass("btn-success").addClass("btn-default").addClass("following").text("已关注")
				} else {
					new_href = data['url'];
					window.location.href = new_href;
				}
			}
		});
	});

	$(".info").on("click",".following",function(){
		var followed = $(".article > .author > .avatar").attr("href").split("=")[1];
		var content = {
			"followed":followed
		};
		$.ajax({
			url: "/bbs/cancel_following",
			type: "POST",
			data: content,
			dataType: "json",
			success: function (data) {
				if(data['status']){
					$(".following").removeClass("following").removeClass("btn-default").addClass("btn-success").addClass("follow").text("关注");
				} else {
					new_href = 'bbs/signup' ;
					window.location.href = new_href;
				}
			}
		});
	});

}