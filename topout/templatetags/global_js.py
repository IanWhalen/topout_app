from django import template
import settings

register = template.Library()

class ShowGoogleAnalyticsJS(template.Node):
	def render(self, context):
		code =  getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
		if not code:
			return "<!-- Google Analytics not included because you haven't set the settings.GOOGLE_ANALYTICS_CODE variable! -->"

		if settings.DEBUG:
			return "<!-- Google Analytics not included because you are in Debug mode! -->"

		return """
            <script type="text/javascript">
              var _gaq = _gaq || [];
              _gaq.push(['_setAccount', '""" + str(code) + """']);
              _gaq.push(['_trackPageview']);

              (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
              })();
            </script>
            <!--End Google Analytics Async Code-->
            """

@register.tag(name='google_analytics')
def google_analytics(parser, token):
	return ShowGoogleAnalyticsJS()

class ShowUserVoiceJS(template.Node):
    def render(self, context):
        return """
          <script type="text/javascript">
          var uservoiceOptions = {
            /* required */
            key: 'thetopout',
            host: 'thetopout.uservoice.com',
            forum: '101243',
            showTab: true,
            /* optional */
            alignment: 'left',
            background_color:'#86C543',
            text_color: 'white',
            hover_color: '#CCC',
            lang: 'en'
          };

          function _loadUserVoice() {
            var s = document.createElement('script');
            s.setAttribute('type', 'text/javascript');
            s.setAttribute('src', ("https:" == document.location.protocol ? "https://" : "http://") + "cdn.uservoice.com/javascripts/widgets/tab.js");
            document.getElementsByTagName('head')[0].appendChild(s);
          }
          _loadSuper = window.onload;
          window.onload = (typeof window.onload != 'function') ? _loadUserVoice : function() { _loadSuper(); _loadUserVoice(); };
          </script>
          """
@register.tag(name='userVoice')
def userVoice(parser, token):
    return ShowUserVoiceJS()
