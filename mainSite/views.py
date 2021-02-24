""" ----------------------  imports  ---------------------------- """

from langdetect import detect
import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from GoogleNews import GoogleNews

from .parser import *
from .serializers import *
from .models import *
from .NeuralNetwork import *
from .settings import *

""" ----------------------- initialising variables -------------------- """

neuralNetwork = NeuralNetwork()


def find(request):
    if request.method == 'GET':
        just_counter = 0
        theme = request.GET['them']

        arrayToReturn = []
        googlenews = GoogleNews()
        seleniumParser = SeleniumParser()
        articleTitleArray = ''
        articleDescriptionArray = ''
        articleMediaArray = ''
        articleLinkArray = ''

        for site in sites:
            googlenews.clear()
            googlenews = GoogleNews(lang='ru')
            googlenews.search(theme + " " + site)
            googlenews.get_page(1)
            for result in googlenews.results():

                if sites.__contains__(result['media']):
                    articleTitleArray += result['title'] + '<break>'
                    articleDescriptionArray += result['desc'] + '<break>'
                    articleMediaArray += result['media'] + '<break>'
                    articleLinkArray += result['link'] + '<break>'

                """description_of_article = [result["desc"]]
                title_of_article = [result["title"]]
                all_of_article = [result["title"] + result["desc"]]
                media = result["media"]

                if media != "Lenta" and media != "РИА Новости" and media != "РБК" and media != "Meduza": continue

                if request.GET.get('q') is None:
                    if media == "Lenta":
                        seleniumParser.parseLenta(result["link"])
                    if media == "Meduza":
                        seleniumParser.parseMeduza(result["link"])

                flagToBreak = False
                for item in dataa:
                    if title_of_article[0] == item["title"]:
                        flagToBreak = True
                        break
                if flagToBreak: continue

                # print(title_of_article)
                # tone = test_tweet(str(title_of_article))
                # tone2 = test_tweet(str(description_of_article))
                # tone3 = test_tweet(str(all_of_article))
                # tone4 = test_article_better(str(title_of_article), str(description_of_article))
                tone5 = neuralNetwork.test_article_the_best(str(title_of_article), str(description_of_article))
                tone6 = neuralNetwork.test_article_the_best_modern(str(title_of_article), str(description_of_article))

                just_counter += 1
                dataa.append({"title": title_of_article[0], "description": description_of_article[0],
                              "url": result["link"],
                              "toneTitle": ("заголовок : " + tone),
                              "toneDescription": ("описание : " + tone2),
                              "toneAll": ("в общем : " + tone3),
                              "toneAve": ("тональность : " + tone4),
                              "toneAveBest": ("тональность : " + tone5[0]),
                              "toneWithBadWordsAveBest": ("тон с ПС: " + tone6[0]),
                              "typeBox": (tone5[1]),
                              "counter": just_counter})"""

        lemmazAllArticles = myLemm.lemmatize(regex.sub('', articleTitleArray).lower() + "<end>" + regex.sub('', articleDescriptionArray))
        articleTitleArrayLemma, articleDescriptionArrayLemma = (''.join(lemmazAllArticles)).split('<end>')
        articleTitleArray = articleTitleArray.split('<break>')
        articleDescriptionArray = articleDescriptionArray.split('<break>')

        articleDescriptionArrayLemma = articleDescriptionArrayLemma.split('<break>')
        articleTitleArrayLemma = articleTitleArrayLemma.split('<break>')
        articleLinkArray = articleLinkArray.split('<break>')
        countOfArticlse = len(articleTitleArray)
        for i in range(countOfArticlse):
            print(i)
            # проверка на наличие такой же статьи
            flagToBreak = False
            for item in arrayToReturn:
                if articleTitleArray[i] == item["title"]:
                    flagToBreak = True
                    break
            if flagToBreak: continue

            tone5 = neuralNetwork.test_article_the_best(str([articleTitleArrayLemma[i]]), str([articleDescriptionArrayLemma[i]]))
            tone6 = neuralNetwork.test_article_the_best_modern(str([articleTitleArrayLemma[i]]), str([articleDescriptionArrayLemma[i]]))

            just_counter += 1
            arrayToReturn.append({"title": articleTitleArray[i], "description": articleDescriptionArray[i],
                          "url": articleLinkArray[i],
                          "toneAveBest": ("тональность : " + tone5[0]),
                          "toneWithBadWordsAveBest": ("тон с ПС: " + tone6[0]),
                          "typeBox": (tone5[1]),
                          "counter": just_counter})

        data = {"message": arrayToReturn, "theme": theme}
        if len(arrayToReturn) == 0:
            return render(request, "mainSite/not_found_page.html", context=data)

        return render(request, "mainSite/showThems.html", context=data)


def hello(request):
    return render(request, 'mainSite/index.html', context={})


class NewsView(APIView):

    def get(self, request, theme):

        news = []
        googlenews = GoogleNews(lang='ru')

        for site in sites:

            googlenews.search(theme + " " + site)
            googlenews.get_page(1)

            for result in googlenews.results():
                item = News()

                description_of_article = [result["desc"]]
                title_of_article = [result["title"]]
                media = result["media"]

                if media != "Lenta" and media != "РИА Новости" and media != "РБК" and media != "Meduza": continue

                """flagToBreak = False
                for item in dataa:
                    if title_of_article[0] == item["title"]:
                        flagToBreak = True
                        break
                if flagToBreak: continue"""

                tone5 = neuralNetwork.test_article_the_best_api(str(title_of_article), str(description_of_article))

                item.title = title_of_article[0]
                item.body = description_of_article[0]
                item.url = result["link"]
                item.rating = tone5

                news.append(item)

            serializer = NewsSerializer(news, many=True)
            return Response({"status": "ok", "news": serializer.data})

        def post(self, request):
            article = request.data.get('article')
            # Create an article from the above data
            serializer = NewsSerializer(data=article)
            if serializer.is_valid(raise_exception=True):
                article_saved = serializer.save()
            return Response({"success": "Article '{}' created successfully".format(article_saved.title)})


class UserCheck(APIView):
    def post(self, request):
        found_user_with_login = False
        checking_user = request.data.get("user")
        users = Person.objects.all()

        for user in users:
            if user.login == checking_user["login"]:
                found_user_with_login = True
                if user.password == checking_user["password"]:
                    serializer = UserSerializer(user)
                    return Response({"status": "ok", "user": serializer.data})

        if found_user_with_login:
            return Response({"status": "bad request", "trouble": "password is incorrect"})
        else:
            return Response({"status": "bad request", "trouble": "no user with such login"})


class UserView(APIView):

    def get(self, request):
        users = Person.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request):
        user_checking = request.data.get("user")
        serializer = UserSerializer(data=user_checking)
        if serializer.is_valid(raise_exception=True):
            users = Person.objects.all()
            for user in users:
                if user.login == user_checking["login"]:
                    return Response({"status": "bad response", "trouble": "User with such login is already exists"})

        serializer.save()
        return Response({"status": "ok"})

    def put(self, request, pk):
        saved_article = get_object_or_404(Person.objects.all(), pk=pk)
        data = request.data.get('user')
        serializer = UserSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({
            "status": "ok", "user": serializer.data
        })

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Person.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Person with id `{}` has been deleted.".format(pk)
        }, status=204)
