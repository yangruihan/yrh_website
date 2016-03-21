import misaka as m

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from misaka import HtmlRenderer, Markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
 
class ColorRenderer(HtmlRenderer):
    def block_code(self, text, lang):
        if not lang:
            return '<pre><code>%s</code></pre>' % text.strip()
        lexer = get_lexer_by_name(lang, stripall = True)
        return highlight(text, lexer, HtmlFormatter())
 
register = template.Library()  # 自定义filter时必须加上
  
@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    flags = m.HTML_HARD_WRAP
    exts = m.EXT_FENCED_CODE | m.EXT_AUTOLINK | m.EXT_NO_INTRA_EMPHASIS | m.EXT_SUPERSCRIPT | m.EXT_TABLES 
    md = Markdown(ColorRenderer(flags), exts)
    return mark_safe(md(value))