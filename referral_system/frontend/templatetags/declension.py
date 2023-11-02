from django import template

register = template.Library()


@register.filter()
def declension(num: int) -> str:
    """Фильтр для склонения слова в зависимости от количества."""

    def f1(x): return (x % 100)//10 != 1 and x % 10 == 1
    def f2(x): return (x % 100)//10 != 1 and x % 10 in [2, 3, 4]
    return ("приглашение" if f1(num) else "приглашения"
            if f2(num) else "приглашений")
