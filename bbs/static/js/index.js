$(function(){
	pageChangeRotate();
	cancleFollow();
	goTop();
	loadMoreArticle();
	following();
});

function pageChangeRotate(){
	var page_change = $(".page-change");
	var img = $(".page-change > img")	;
	page_change.on("click",function(){
		img.addClass("page-change-rotate").animate({height:"auto"},function(){
			$(this).removeClass("page-change-rotate")
		});
		change_author()
	})
}

function change_author() {
	$.ajax({
		url:'/bbs/change_recommend_author',
		type:'GET',
		dataType:'json',
		success:function (data){
			var content = $(".recommended-authors > .list");
			content.empty();
			var authors = data['authors'];
			var domain = window.location.protocol + '//' + window.location.host;
			var index, _str;
			for (index in authors){
				_str = '<li>' +
							'<a href="' + domain + '/bbs/main_page?user=' + String(authors[index]['id']) + '" class="avatar">' +
								'<img src="' + domain + '/media/' + String(authors[index]['head_img']) + '"/>' +
							'</a>' +
							'<a href="javascript:void(0);" class="follow">关注</a>' +
							'<a href="' + domain + '/bbs/main_page?user=' + String(authors[index]['id']) + '" class="name">' + authors[index]['name'] + '</a>' +
							'<p>写了' + authors[index]['words'] + '字 · ' + authors[index]['loved'] + '喜欢</p>' +
						'</li>';
				content.append(_str);
			}
		}
	})
}


function cancleFollow(){
	$(".list > li").on("mousemove",".following",function(){
		$(this).text("取消关注")
	});
	
	$(".list > li").on("mouseout",".following",function(){
		$(this).text("已关注");
	})
}


function goTop(){
	$(document).scroll(function(){	
		var top = $(document).scrollTop();
		var side_tool = $(".side-tool li");
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
	
	var side_tool = $(".side-tool li");
	side_tool.on("click",function(){
            $('body,html').animate({scrollTop:0},300);	
	})
}

function loadMoreArticle() {
	$(".container-left > .load-more").on("click",function () {
		content = {
			"offset":$(this).attr("data-offset")
		};
		if (content['offset'] == 0){
			return false;
		}
		$.ajax({
			url:'/bbs/load_more_article',
			type:'GET',
			dataType:'json',
			data:content,
			success:function (data){
				var load_btn= $(".container-left > .load-more");
				var offset  = data['offset'];
				if (!data['status']){
					load_btn.attr("data-offset", 0);
					load_btn.text("到底了");
					return false;
				}
				var articles = data['article'];
				var content = $('.list-container > .note-list');
				var domain = window.location.protocol + '//' + window.location.host;
				var index, _str, _str1, _str2;
				for (index in articles){
					if(articles[index]['have_img']){
						_str1 = '<li class="have-img">' +
								'<a class="wrap-img" href="' + domain + '/bbs/article/'+ String(articles[index]['id']) + '">'+
								'<img src="' + domain + '/media/' + String(articles[index]['have_img'])+ '"/></a>'
					} else {
						_str1 = '<li>'
					}
					_str2 = '<div class="content">' +
							'<a class="title" href="' + domain + '/bbs/article/'+ String(articles[index]['id']) + '">' + articles[index]['title'] + '</a>' +
							'<p class="abstract">' + articles[index]['abstract'] + '</p>' +
							'<div class="meta">' +
							'<a href="" target="_blank" class="nickname">'+ articles[index]['user_name'] + '</a>' +
							'<span class="comment">' +
							'<img src="' + domain + '/static/img/comment.svg"/>' +
							'<span>' + '&nbsp;' + String(articles[index]['comments']) + '</span>' +
							'</span>' +
							'<span class="collect">' +
							'<img src="' + domain + '/static/img/like.svg"/>' +
							'<span>' + '&nbsp;' + String(articles[index]['love']) + '</span>' +
							'</span>' +
							'</div>' +
							'</div>' +
							'</li>';
					_str = _str1 + _str2;
					content.append(_str);
				}
				load_btn.attr("data-offset", offset);
			}
		})
	})
}

function following() {
	$(".recommended-authors .list").on("click", "li .follow",function () {
		var followed = $(this).siblings(".name").attr("href").split("=")[1];
		var content = {
			"followed":followed
		};
		var obj = $(this);
		$.ajax({
			url: "/bbs/set_following",
			type: "POST",
			data: content,
			dataType: "json",
			success: function (data) {
				if(data['status']){
					$(obj).text("已关注").removeClass("follow").addClass("following");
				} else {
					new_href = 'bbs/signup' ;
					window.location.href = new_href;
				}
			}
		})
	});

	$(".recommended-authors .list").on("click", "li .following",function () {
		var followed = $(this).siblings(".name").attr("href").split("=")[1];
		var content = {
			"followed":followed
		};
		var obj = $(this);
		$.ajax({
			url: "/bbs/cancel_following",
			type: "POST",
			data: content,
			dataType: "json",
			success: function (data) {
				if (data['status']){
					$(obj).text("关注").removeClass("following").addClass("follow");
				} else {
					new_href = 'bbs/signup' ;
					window.location.href = new_href;
				}
			}
		})
	});
}