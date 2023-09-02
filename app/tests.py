import datetime
from .views import *
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import csv

from .models import Question, Molecule


def create_molecule():
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    time = timezone.now()
    content ="""\\chemfig{
            % 1
      -[:42]N% 2
      -[:96]% 3
     =_[:24]N% 4
     -[:312]% 5
    =_[:240]% 6
               (
         -[:168]\\phantom{N}% -> 2
               )
     -[:300]% 7
               (
         =[:240]O% 8
               )
           -N% 9
               (
         -[:300]% 14
               )
      -[:60]% 10
               (
               =O% 11
               )
     -[:120]N% 12
               (
         -[:180]% -> 5
               )
      -[:60]% 13}"""

    return Molecule.objects.create(id=0,name="Arsenic",content=content, creat_date=time)

def fill_molecule_db():
      time = timezone.now()
      i = 0
      file_reader= open('app/data/molecule.csv', "rt")
      read = csv.reader(file_reader)
      for row in read :
        if (i != 0):
          Molecule.objects.create(id=row[0],name=row[1],content=row[2], creat_date=time)
        i = i+1

class DrawingTest(TestCase):

    def test_draw_arc(self):
        print("test_draw_arc ...")
        parameters = [""]
        arc = drawArc(parameters)
        self.assertEqual(arc, "todo")
        print("OK")

    def test_draw_arrow(self):
        print("test_draw_arrow ...")
        parameters = [""]
        arrow = drawArrow(parameters)
        self.assertEqual(arrow, "todo")
        print("OK")

    def test_draw_circle(self):
        print("test_draw_circle ...")
        parameters = [""]
        circle = drawCircle(parameters)
        self.assertEqual(circle, "todo")
        print("OK")

    def test_draw_diamond(self):
        print("test_draw_diamond ...")
        parameters = [""]
        diamond = drawDiamond(parameters)
        self.assertEqual(diamond, "todo")
        print("OK")

    def test_draw_ellipse(self):
        print("test_draw_ellipse ...")
        parameters = [""]
        ellipse = drawEllipse(parameters)
        self.assertEqual(ellipse, "todo")
        print("OK")

    def test_draw_graph(self):
        print("test_draw_graph ...")
        parameters = [""]
        graph = drawGraph(parameters)
        self.assertEqual(graph, "todo")
        print("OK")

    def test_draw_line(self):
        print("test_draw_line ...")
        parameters=[1,1,1,1,1,1,1]
        line = drawLine(parameters)

        result = (
            "\\draw[color=custom_color] (0,0) -- (1,0) ;%(x1,y1) -- (x2,y2)%")
        self.assertEqual(line, result)
        print("OK")

    def test_draw_molecule(self):
        print("test_draw_molecule ...")
        create_molecule()
        parameters = [0,0]
        theorical_result = """\\chemfig{
            % 1
      -[:42]N% 2
      -[:96]% 3
     =_[:24]N% 4
     -[:312]% 5
    =_[:240]% 6
               (
         -[:168]\\phantom{N}% -> 2
               )
     -[:300]% 7
               (
         =[:240]O% 8
               )
           -N% 9
               (
         -[:300]% 14
               )
      -[:60]% 10
               (
               =O% 11
               )
     -[:120]N% 12
               (
         -[:180]% -> 5
               )
      -[:60]% 13}"""
        molecule = drawMolecule(parameters)
        self.assertEqual(molecule, theorical_result)
        print("OK")

    def test_molecule_compile(self):
        print("test_molecule_compile ...")
        fill_molecule_db()
        for field in Molecule.objects.all():
          print("test_molecule_compile : "+ field.name +" ...")
          id = field.id
          molecule = get_object_or_404(Molecule, id=id)
          selected_type = 'mol'
          file = open("app/templates/app/temp.tex","w")
          customcolor="230,230,23"
          scale=[1,-1]
          parameters=[1,id,1,1,1,1,1]
          print(id)
          documentclass = (
              "\\RequirePackage{luatex85}\n\\documentclass[border = 1 cm]{standalone}")
          color = "\\definecolor{{custom_color}}{{RGB}}{{{c}}}".format(c=customcolor)
          additionnal_shortcuts = (
            "\\newlength{\\mcfvspace}\n\\setlength{\\mcfvspace}{1.5pt} \n\\newcommand{\\mcfabove}[2]{\\chemabove[\\mcfvspace]{ #1}{ #2}}\n\\newcommand{\\mcfbelow}[2]{\\chembelow[\\mcfvspace]{ #1}{ #2}}\n\\newcommand{\\mcfplus}{+}\n\\newcommand{\\mcfminus}{-}\n\\newlength{\\boxwidth}\n\\newlength{\\boxheight}\n\\newcommand{\\boxmcf}[3][l]{ \n\\settowidth{\\boxwidth}{\\printatom{ #2}} \n\\settoheight{\\boxheight}{\\printatom{ #2}} \n\\makebox[\\boxwidth][ #1]{\\raisebox{0pt}[\\boxheight][0pt]{\\printatom{ #3}}}} \n\\newcommand{\\mcfleft}[2]{\\boxmcf[r]{ #2}{ #1  #2}} \n\\newcommand{\\mcfright}[2]{\\boxmcf{ #1}{ #1  #2}} \n\\newcommand{\\mcfaboveright}[3]{\\mcfabove{ #1}{\\boxmcf{ #2}{ #2  #3}}} \n\\newcommand{\\mcfbelowright}[3]{\\mcfbelow{ #1}{\\boxmcf{ #2}{ #2  #3}}}")
          comment = "%You can modify your color here%"
          begindoc = "\\begin{document}"
          packages = "\\usepackage{chemfig}"
          beginenv = ""
          endenv = ""
          scale = ""
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

          file.write(chaine)
          file.close()

          url = reverse('app:latex_converter_pdf')
          response = self.client.get(url)
          self.assertEqual(response.status_code, 200)
          print("OK")
        print("OK")

    def test_draw_parallelogram(self):
        print("test_draw_parallelogram ...")
        parameters = [""]
        parallelogram = drawParallelogram(parameters)
        self.assertEqual(parallelogram, "todo")
        print("OK")

    def test_draw_polygon(self):
        print("test_draw_polygon ...")
        parameters = [""]
        polygon = drawPolygon(parameters)
        self.assertEqual(polygon, "todo")
        print("OK")

    def test_draw_rectangle(self):
        print("test_draw_rectangle ...")
        parameters = [""]
        rectangle = drawRectangle(parameters)
        self.assertEqual(rectangle, "todo")
        print("OK")

    def test_draw_star(self):
        print("test_draw_star ...")
        parameters = [""]
        star = drawStar(parameters)
        self.assertEqual(star, "todo")
        print("OK")

    def test_draw_trapeze(self):
        print("test_draw_trapeze ...")
        parameters = [""]
        trapeze = drawTrapeze(parameters)
        self.assertEqual(trapeze, "todo")
        print("OK")

    def test_draw_tree(self):
        print("test_draw_tree ...")
        parameters = [""]
        tree = drawTree(parameters)
        self.assertEqual(tree, "todo")
        print("OK")

    def test_dico(self):
        print("test_dico ...")
        create_molecule()
        practice_result = [0]*14
        theorical_result = ['todo']*14
        theorical_result[6] = (
            "\\draw[color=custom_color] (0,0) -- (1,0) ;%(x1,y1) -- (x2,y2)%")
        theorical_result[7] = """\\chemfig{
            % 1
      -[:42]N% 2
      -[:96]% 3
     =_[:24]N% 4
     -[:312]% 5
    =_[:240]% 6
               (
         -[:168]\\phantom{N}% -> 2
               )
     -[:300]% 7
               (
         =[:240]O% 8
               )
           -N% 9
               (
         -[:300]% 14
               )
      -[:60]% 10
               (
               =O% 11
               )
     -[:120]N% 12
               (
         -[:180]% -> 5
               )
      -[:60]% 13}"""

        parameters=[1,0,1,1,1,1,1]
        type = ['arc','arr', 'cir','dia','ell','gra','lin',
        'mol','par','pol','rec','sta','tra','tre']

        for i in range(0,14):
            practice_result[i] = dico_draw(type[i],parameters)
            self.assertEqual(practice_result[i], theorical_result[i])
        print("OK")






























# class QuestionModelTests(TestCase):

#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)

#     def test_was_published_recently_with_old_question(self):
# 	    """
# 	    was_published_recently() returns False for questions whose pub_date
# 	    is older than 1 day.
# 	    """
# 	    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
# 	    old_question = Question(pub_date=time)
# 	    self.assertIs(old_question.was_published_recently(), False)

#     def test_was_published_recently_with_recent_question(self):
# 	    """
# 	    was_published_recently() returns True for questions whose pub_date
# 	    is within the last day.
# 	    """
# 	    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
# 	    recent_question = Question(pub_date=time)
# 	    self.assertIs(recent_question.was_published_recently(), True)


# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)


# class QuestionIndexViewTests(TestCase):

#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('app:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('app:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('app:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])

#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('app:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )

#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('app:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )

# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future
#         returns a 404 not found.
#         """
#         future_question = create_question(question_text='Future question.', days=5)
#         url = reverse('app:detail', args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)

#     def test_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past
#         displays the question's text.
#         """
#         past_question = create_question(question_text='Past Question.', days=-5)
#         url = reverse('app:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)