$(function(){
	
	fadeLogo();
	showError();
	
	window.onresize = function(){
		fadeLogo()
	};
	


	
	function fadeLogo(){
		var bw = $(document).width();
//		console.log(bw)
		var logo = $(".sign > .logo");
		if (bw < 780) {
			logo.css({
				"display":"none"
			})
		
		} else{
			logo.css({
				"display":"block"
			})
		}
	}

	function showError() {
		all_width = $(document).width();
		left = (all_width - 200) / 2;
		errors = $(".error-message").text();
		errors_message = errors.split("|");
		for (var index in errors_message){
			if (errors_message[index]){
				__str = '<div class="error">' + errors_message[index] + '</div>';
				$(".signup-container").append(__str);
				$(".signup-container").find(".error").css({
					"left": left
				}).fadeOut(2000);
				return false;
			}
		}
	}
});