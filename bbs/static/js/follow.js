$(function () {
    loadMoreFollowArticle()
});


function loadMoreFollowArticle() {
	$(".container-right > .load-more").on("click",function () {
		content = {
			"offset":$(this).attr("data-offset")
		};
		if (content['offset'] == 0){
			return false;
		}
		$.ajax({
			url:'/bbs/following/load_more_follow_article',
			type:'GET',
			dataType:'json',
			data:content,
			success:function (data){
				var load_btn= $(".container-right > .load-more");
				var offset  = data['offset'];
				if (!data['status']){
					load_btn.attr("data-offset", 0);
					load_btn.text("到底了");
					return false;
				}
				var articles = data['article'];
				var content = $('.container-right > div > .note-list');
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