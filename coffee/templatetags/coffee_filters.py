from django import template

register = template.Library()

@register.filter(name='coffee_tag')
def coffee_tag_filter(value):
    # فلتر مخصص يضيف لمسة قهوة للأسعار
    return f"☕ {value} ر.ي"
@register.filter(name='coffee_footer_msg')
def coffee_footer_msg(value):
    # فلتر مخصص يضيف عبارة مميزة في أسفل الصفحة
    return f"✨ {value} - استمتع بكل شفشفة من قهوتك المفضلة ☕"