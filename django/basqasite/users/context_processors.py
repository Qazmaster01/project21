from basqa.views import menu


def get_basqa_context(request):
    return {'mainmenu': menu}