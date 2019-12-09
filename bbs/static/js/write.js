$(function(){
	InitUMeditor();
	newArticle();
	changeActive();
	delArticle();
	saveArticle();
	publishArticle()
});

function InitUMeditor(){
	var um = UM.getEditor('myEditor',{
		toolbar: ['undo', 'redo','|', 'bold','italic','strikethrough',
		'fontfamily','fontsize','forecolor','backcolor','|','justifyleft','justifycenter','justifyright',
		'horizontal','|','link unlink |','video','image','emotion','|','source','preview','imagecenter'],
		initialFrameHeight: 538,
		initialFrameWidth: 820,
		autoHeightEnabled: false,
		autoFloatEnabled: true,
		'fontsize':[10, 12, 16, 18, 20, 24, 36],
		maxInputCount:10,
		autotypeset:true,
		imageUrl:'bbs/../upload',
		imagePath:'',
	});
}


function newArticle(){
	var new_art = $(".new-article");
	var list = $(".article-list");
	new_art.on("click",function(){
		old = $(".article-list").find(".article-active");
		if (old.length) {
			article_id = old.attr("data-artid");
			var isnum = /^\d+$/.test(article_id);
			if(isnum){
				saveArticleAjax(article_id, false)
			}else {
				setCookie(article_id, UM.getEditor('myEditor').getContent())
			}
		}
		current_url = String(window.location.host);
		now = new Date();
		var data_temp = String.fromCharCode(65 + Math.floor(Math.random()*26)) + String(now.valueOf()).substring(5,13);
		txt = String(now.getFullYear()) +"-"+ String(now.getMonth()+1) +"-"+ String(now.getDate()) +" "+ String(now.getHours()) +":"+ String(now.getMinutes()) +":"+ String(now.getSeconds());
		var _str = '<li class="article article-active"'+ ' data-artid='+ data_temp +'>' +
						'<img src="' + "http://" + current_url + '/static/' + 'img/icon-articles.svg"/>' +
						'<span class="article-title">'+txt+'</span>' +
						'<img src="' + "http://" + current_url + '/static/' + 'img/del.svg" class="delete"/>' +
					'</li>';
		list.children("li").each(function(){
			$(this).removeClass("article-active")
		});
		list.prepend(_str);
		changeTitle();
		UM.getEditor('myEditor').setContent('<p>这里我可以写一些输入提示</p>')
	})
}

function changeActive(){
	var current = $(".container-middle .article-list");
	current.on("click",".article",function(){
		old = $(".article-list").find(".article-active").attr("data-artid");
		var isnum = /^\d+$/.test(old);
		var um = UM.getEditor('myEditor');
		if (isnum){
			saveArticleAjax(old, false);
			$(this).addClass("article-active").siblings().removeClass("article-active");
			changeTitle();
			new_id = $(this).attr("data-artid");
			getArticleAjax(new_id)
		} else {
			setCookie(old, um.getContent());
			$(this).addClass("article-active").siblings().removeClass("article-active");
			changeTitle();
			new_id = $(this).attr("data-artid");
			getArticleAjax(new_id)
		}
	})
}

function getArticleAjax(new_id) {
	var um = UM.getEditor('myEditor');
	if(/^\d+$/.test(new_id)){
		content = {
			'id':new_id
		};
		$.ajax({
			url:'/bbs/write/get',
			type:'POST',
			dataType:'json',
			data:content,
			success:function (data){
				um.setContent(data['body'])
			}
		})
	} else {
		um.setContent(getCookie(new_id))
	}
}

function delArticle(){
	var current = $(".container-middle .article-list");
	current.on("click",".article .delete",function(event){
		var sure = confirm("即将删除文章：" + $(this).siblings("span").text());
		if (sure){
			var article_id = $(this).parent().attr("data-artid");
			if ($(this).parent(".article").hasClass("article-active")) {
				index = $(this).parent(".article").index();
				list = $(this).parent(".article").parent(".article-list");
				all = list.find("li").length;
				$(this).parent(".article").remove();
				if (all == 1) {
					$(".container-right .title").val("");
					delArticleOption(article_id,article_id);
					UM.getEditor('myEditor').setContent('<p>这里我可以写一些输入提示</p>')
				} else if (index +1 == all) {
					list.children().eq(index-1).addClass("article-active");
					new_id = list.children().eq(index-1).attr("data-artid");
					delArticleOption(article_id, new_id);
				} else {
					list.children().eq(index).addClass("article-active");
					new_id = list.children().eq(index).attr("data-artid");
					delArticleOption(article_id, new_id);
				}
			} else {
				$(this).parent(".article").remove();
				delArticleOption(article_id, article_id);
			}
			changeTitle();
		}
		event.stopPropagation();
	})	
}

function delArticleOption(old_id ,new_id) {
    if(String(old_id) == String(new_id)){
		delArticleAjax(old_id)
    } else {
    	delArticleAjax(old_id);
        getArticleAjax(new_id);
	}
}

function delArticleAjax(id) {
    if(/^\d+$/.test(id)){
        content = {
            'id':id
        };
        $.ajax({
            url:'/bbs/write/delete',
            type:'DELETE',
            dataType:'json',
            data:content,
            success:function (data){
                return false;
            }
        })
    } else {
    	Cookie(id)
	}
}

function changeTitle(){
	var title = $(".container-right .title");
	var article = $(".article-list .article");
	var list = $(".article-list");
	article.each(function(){
		if ($(this).hasClass("article-active")) {
			title.val($(this).find("span").text())
		} 
	});
	
	title.on("input propertychange",function(){
		list.find(".article-active .article-title").text(title.val())
	})
}

function saveArticle(){
	$(".save-article").on("click",function () {
		if ($(".article-list").children('li').length==0) {
			alert("没有内容可以保存");
			return false;
		}
		article_id = $(".article-list").children(".article-active").attr("data-artid");
		saveArticleAjax(article_id, true)
	})
}

function saveArticleAjax(article_id, call) {
	article_title = $(".article-list").children(".article-active").children("span").text();
	article_body = UM.getEditor('myEditor').getContent();
	content= {
		'id':article_id,
		'title':article_title,
		'body':article_body
	};
	$.ajax({
		url:'/bbs/write/save',
		type:'POST',
		dataType:'json',
		data:content,
		success:function (data) {
			if(call){
				if (data['virtual_id'] == data['article_id']){
					alert("保存成功");
					return false;
				}else{
					$(".article-list").children(".article-active").attr("data-artid",data['article_id']);
					Cookie(data['virtual_id']);
					alert("保存成功");
				}
			}
		}
	})
}

function publishArticle() {
	$(".publish-article").on("click",function () {
		if ($(".article-list").children('li').length==0) {
			alert("没有内容可以发布");
			return false;
		}
		article_id = $(".article-list").children(".article-active").attr("data-artid");
		publishArticleAjax(article_id)
	})
}


function publishArticleAjax(article_id) {
	article_title = $(".article-list").children(".article-active").children("span").text();
	article_body = UM.getEditor('myEditor').getContent();
	content= {
		'id':article_id,
		'title':article_title,
		'body':article_body
	};
	$.ajax({
		url:'/bbs/write',
		type:'POST',
		async:false,
		dataType:'json',
		data:content,
		success:function (data) {
			if (!/^[0-9]+$/.test(article_id)){
				Cookie(article_id)
			}
			new_href = 'article/' + String(data['article_id']);
			window.location.href = new_href
		}
	})
}


//获取cookie，参数name指定要获取的cookie的名称
function getCookie(name) {
    var start = document.cookie.indexOf(name + "="); //得到cookie字符串中的名称
    var len = start + name.length + 1; //得到从起始位置到结束cookie位置的长度
    //如果起始没有值且name不存在于cookie字符串中，则返回null
    if ((!start) && (name != document.cookie.substring(0, name.length))) {
        return null;
    }
    if (start == -1) return null; //如果起始位置为-1也为null
    var end = document.cookie.indexOf(';', len); //获取cookie尾部位置
    if (end == -1) end = document.cookie.length; //计算cookie尾部长度
    return unescape(document.cookie.substring(len, end)); //获取cookie值
}
//设置cookie，name为名称，value为值，expires为过期日，path为路径，domain为域名，secure为加密
function setCookie(name, value, expires, path, domain, secure) {
    var today = new Date();
    today.setTime(today.getTime());
    if (expires) {
        expires = expires * 1000 * 60 * 60 * 24; //计算cookie的过期毫秒数
    }
    //计算cookie的过期日期
    var expires_date = new Date(today.getTime() + (expires));
    //构造并保存cookie字符串
    document.cookie = name + '=' + escape(value) +
        ((expires) ? ';expires=' + expires_date.toGMTString() : '') + //expires.toGMTString()
        ((path) ? ';path=' + path : '') +
        ((domain) ? ';domain=' + domain : '') +
        ((secure) ? ';secure' : '');
}
//删除cookie，必须先获取指定名称的cookie，然后让cookie过期
function Cookie(name, path, domain) {
    if (getCookie(name)) document.cookie = name + '=' +
        ((path) ? ';path=' + path : '') +
        ((domain) ? ';domain=' + domain : '') +
        ';expires=Thu, 01-Jan-1970 00:00:01 GMT';
}