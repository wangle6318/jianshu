# jianshu
version-1.1
django实现的仿简书网站
1、利用的工具：jquery,django，django-notification-hq
2、主要页面：未登陆状态可访问：首页、文章页、其他人信息页、其他人喜欢的文章页、登陆、注册
            登陆状态：首页、文章页、其他人信息页、其他人喜欢的文章页、登陆、注册、关注的人、消息通知、写文章、收藏的文章、喜欢的文章、基本信息设置
3、几个重要的页面介绍：
    1）写文章页：创建文章后，先在本地生成虚拟文章ID，利用本地cookie暂存，浏览器关闭则删除；点击保存后上传到服务器端，创建真实ID，返回前端把虚拟ID变为真实ID。
                