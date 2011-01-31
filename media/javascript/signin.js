// http://blog.stannard.net.au/2011/01/07/creating-a-form-with-labels-inside-text-fields-using-jquery/

$(document).ready(function(){
		 
	$("form#login-form input")
		.bind("focus.labelFx", function(){
			$(this).prev().hide();
		})
		.bind("blur.labelFx", function(){
			$(this).prev()[!this.value ? "show" : "hide"]();
		})
		.trigger("blur.labelFx");
});
