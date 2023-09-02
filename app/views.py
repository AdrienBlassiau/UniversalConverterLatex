from django.http import Http404, HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django_tex.core import compile_template_to_pdf
from django_tex.views import render_to_pdf

from django.utils import timezone

from .models import Question, Choice, LatexDoc, Molecule

from django.template.loader import render_to_string

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'app/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'app/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('app:results', args=(question.id,)))

def manage_dropdown(request):
    data = request.GET.get('input')
    if (data=='aff1'):
        answer = render_to_string('app/formulaires/formulaire_cercle.html',{})
    elif (data=='aff2'):
        answer = render_to_string('app/formulaires/formulaire_triangle.html',{})
    elif (data=='aff3'):
        answer = render_to_string('app/formulaires/formulaire_point.html',{})
    elif (data=='aff4'):
        answer = render_to_string('app/formulaires/formulaire_cercle.html',{})
    else:
        answer = render_to_string('app/formulaires/formulaire_triangle.html',{})
    data = {
    'respond': answer
    }
    return JsonResponse(data)

def drawArc(parameters):
    '''
    This function create a arc with tikz with some parameters
    '''
    return "todo"

def drawArrow(parameters):
    '''
    This function create an arrow with tikz with some parameters
    '''
    return "todo"

def drawCircle(parameters):
    '''
    This function create a circle with tikz with some parameters
    '''
    return "todo"

def drawDiamond(parameters):
    '''
    This function create a diamond with tikz with some parameters
    '''
    return "todo"

def drawEllipse(parameters):
    '''
    This function create an ellipse tikz with some parameters
    '''
    return "todo"

def drawGraph(parameters):
    '''
    This function create a graph tikz with some parameters
    '''
    return "todo"

def drawLine(parameters):
    '''
    This function create a line with tikz with some parameters
    '''
    line="\\draw[color=custom_color] (0,0) -- ({t},0) ;".format(t=parameters[0])
    comment="%(x1,y1) -- (x2,y2)%"
    return line+comment

def drawMolecule(parameters):
    '''
    This function create a molecule with tikz with some parameters
    '''
    molecule = get_object_or_404(Molecule, pk=parameters[1])
    code = molecule.content
    return code

def drawParallelogram(parameters):
    '''
    This function create a parallelogram with tikz with some parameters
    '''
    return "todo"

def drawPolygon(parameters):
    '''
    This function create a polygon with tikz with some parameters
    '''
    return "todo"

def drawRectangle(parameters):
    '''
    This function create a rectangle with tikz with some parameters
    '''
    return "todo"

def drawStar(parameters):
    '''
    This function create a star with tikz with some parameters
    '''
    return "todo"

def drawTrapeze(parameters):
    '''
    This function create a trapeze with tikz with some parameters
    '''
    return "todo"

def drawTree(parameters):
    '''
    This function create a tree with tikz with some parameters
    '''
    return "todo"

def dico_draw(selected_type,parameters):
    '''
    This function draw what we want, using a dictionnary
    '''
    return {
        'arc':drawArc(parameters),
        'arr':drawArrow(parameters),
        'cir':drawCircle(parameters),
        'dia':drawDiamond(parameters),
        'ell':drawEllipse(parameters),
        'gra':drawGraph(parameters),
        'lin':drawLine(parameters),
        'mol':drawMolecule(parameters),
        'par':drawParallelogram(parameters),
        'pol':drawPolygon(parameters),
        'rec':drawRectangle(parameters),
        'sta':drawStar(parameters),
        'tra':drawTrapeze(parameters),
        'tre':drawTree(parameters),
    }.get(selected_type, drawLine(parameters))
    #We can choose a default return, drawLine(parameters) here ...



def latex_converter_string_to_pdf(request):
    '''
    This function take the informations about what we want to draw, draw it
    and return to index.html the right to draw the newfileobject
    '''

    selected_type = 'mol'
    #choice has to be in CONTENT_FORMAT_CHOICES (see models), it will be =>
    #request.POST['choice']

    file = open("app/templates/app/temp.tex","w")


    customcolor="230,230,23"
    #an rgb color, or other format if you want
    #=>request.POST['color'] : **COLOR TASK**
    scale=[1,-1]
    #the scale of our drawing
    #=>request.POST['scale'] : **SCALE TASK**
    parameters=[1,542,1,1,1,1,1]
    #Some parameters from the form (for instance : size, angle, ...)
    #=>request.POST['parameters'] or with different post ...


    documentclass = (
        "\\RequirePackage{luatex85}\n\\documentclass[border = 1 cm]{standalone}")

    color = "\\definecolor{{custom_color}}{{RGB}}{{{c}}}".format(c=customcolor)
    comment = "%You can modify your color here%"

    begindoc = "\\begin{document}"

    if (selected_type == 'mol'):
        packages = "\\usepackage{chemfig}"
        additionnal_shortcuts = (
            "\\newlength{\\mcfvspace}\n\\setlength{\\mcfvspace}{1.5pt} \n\\newcommand{\\mcfabove}[2]{\\chemabove[\\mcfvspace]{ #1}{ #2}}\n\\newcommand{\\mcfbelow}[2]{\\chembelow[\\mcfvspace]{ #1}{ #2}}\n\\newcommand{\\mcfplus}{+}\n\\newcommand{\\mcfminus}{-}\n\\newlength{\\boxwidth}\n\\newlength{\\boxheight}\n\\newcommand{\\boxmcf}[3][l]{ \n\\settowidth{\\boxwidth}{\\printatom{ #2}} \n\\settoheight{\\boxheight}{\\printatom{ #2}} \n\\makebox[\\boxwidth][#1]{\\raisebox{0pt}[\\boxheight][0pt]{\\printatom{ #3}}}} \n\\newcommand{\\mcfleft}[2]{\\boxmcf[r]{ #2}{ #1#2}} \n\\newcommand{\\mcfright}[2]{\\boxmcf{ #1}{ #1#2}} \n\\newcommand{\\mcfaboveright}[3]{\\mcfabove{ #1}{\\boxmcf{ #2}{ #2#3}}} \n\\newcommand{\\mcfbelowright}[3]{\\mcfbelow{ #1}{\\boxmcf{ #2}{ #2#3}}}")
        beginenv = ""
        endenv = ""
        scale = ""
    else:
        scale = "[xscale={x},yscale={y}]".format(x=scale[0],y=scale[1])
        additionnal_shortcuts = ""
        packages = "\\usepackage{tikz}"
        beginenv = "\\begin{tikzpicture}"
        endenv = "\\end{tikzpicture}"

    enddoc = "\\end{document}"

    choice = dico_draw(selected_type,parameters)

    chaine = (
        documentclass+"\n"+
        packages+"\n"+
        color+comment+"\n"+
        additionnal_shortcuts+"\n"+
        begindoc+"\n"+
        beginenv+scale+"\n"+
        choice+"\n"+
        endenv+"\n"+
        enddoc )

    newfileobject = LatexDoc(content=choice,
                        creat_date=timezone.now(),
                        latex_type=selected_type)
    #We create a row in our database

    newfileobject.save()
    #We save our drawing on the database

    file.write(chaine)
    file.close()

    return render(request, 'app/index.html',
        {'dessin_commande': "ok",'latex_objet': newfileobject})

def latex_converter_pdf(request):
    '''
    This return a pdf with what we want to draw
    '''
    template_name = 'app/temp.tex'
    context = {}
    return render_to_pdf(request, template_name, context, filename='temp.pdf')
