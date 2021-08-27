from django.shortcuts import render, HttpResponse, redirect

from trader.models import Variants, Position

from icecream import ic
from datetime import datetime

from .view import engine, varian_stats, plots



def main(request):
    if request.GET.get('del'):
        Position.objects.filter(varian=Variants.objects.get(id=request.GET['del']).name).delete()
        Variants.objects.filter(id=request.GET['del']).update(finish=False, sharp=None)

        return redirect('/')
    elif request.GET.get('reset_all'):
        Position.objects.all().delete()
        Variants.objects.all().update(finish=False,sharp=None)
        return redirect('/')


    list_varian = Variants.objects.all()

    list_varians=varian_stats.get_varian_stats(list_varian)


    return render(request, 'trader/main.html',
                  {'list_varians': list_varians})


def update_server(request):
    import git
    if True:
        try:
            repo = git.Repo('/home/drann/bot')
        except:
            repo = git.Repo('/Users/user/bot/')
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse('Updated PythonAnywhere successfully', 200)
    else:
        return HttpResponse('Wrong event type', 400)

def varian_view(request):
    context={}
    varian=Variants.objects.get(id=request.GET.get('varian'))

    context['varian']=varian_stats.get_varian_stats([varian,])[0]

    context['graph'] = plots.get_chart_varian(varian)

    if not varian.sharp:
        varian_stats.get_detail_stats(varian)

    return render(request, 'trader/varian.html',context)




