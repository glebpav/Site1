""" ----------------------  imports  ---------------------------- """
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from GoogleNews import GoogleNews
from pygooglenews import GoogleNews as GN

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

        lemmazAllArticles = myLemm.lemmatize(
            regex.sub('', articleTitleArray).lower() + "<end>" + regex.sub('', articleDescriptionArray))
        articleTitleArrayLemma, articleDescriptionArrayLemma = (''.join(lemmazAllArticles)).split('<end>')
        articleTitleArray = articleTitleArray.split('<break>')
        articleDescriptionArray = articleDescriptionArray.split('<break>')
        articleMediaArray = articleMediaArray.split('<break>')

        articleDescriptionArrayLemma = articleDescriptionArrayLemma.split('<break>')
        articleTitleArrayLemma = articleTitleArrayLemma.split('<break>')
        articleLinkArray = articleLinkArray.split('<break>')
        countOfArticlse = len(articleTitleArray)
        for i in range(countOfArticlse):
            # проверка на наличие такой же статьи
            flagToBreak = False
            for item in arrayToReturn:
                if articleTitleArray[i] == item["title"]:
                    flagToBreak = True
                    break
            if flagToBreak: continue

            textToAlize = 'null'
            if request.GET.get('q') is None:
                if articleMediaArray[i] == "Lenta":
                    textToAlize=seleniumParser.parse_lenta(articleLinkArray[i])
                elif articleMediaArray[i] == "Meduza":
                    textToAlize=seleniumParser.parse_meduza(articleLinkArray[i])
                elif articleMediaArray[i] == "РИА Новости":
                    textToAlize=seleniumParser.parse_ria(articleLinkArray[i])
                if textToAlize != 'null':
                    textToAlize = myLemm.lemmatize(regex.sub('', textToAlize).lower())
                    tone5 = neuralNetwork.test_article_the_best(str([textToAlize]), str([textToAlize]))
                else:
                    tone5 = neuralNetwork.test_article_the_best(str([articleTitleArrayLemma[i]]),
                                                                str([articleDescriptionArrayLemma[i]]))
            else:
                tone5 = neuralNetwork.test_article_the_best(str([articleTitleArrayLemma[i]]),
                                                        str([articleDescriptionArrayLemma[i]]))
            print(articleTitleArrayLemma[i])
            tone6 = neuralNetwork.test_article_the_best_modern(str([articleTitleArrayLemma[i]]),
                                                               str([articleDescriptionArrayLemma[i]]))
            just_counter += 1
            arrayToReturn.append({"title": articleTitleArray[i],
                                  "description": articleDescriptionArray[i],
                                  "url": articleLinkArray[i],
                                  "toneAveBest": ("тональность : " + tone5[0]),
                                  "toneWithBadWordsAveBest": ("тон с ПС: " + tone6[0]),
                                  "typeBox": (tone5[1]),
                                  "counter": just_counter})

        if len(arrayToReturn) == 0:
            return render(request, "mainSite/not_found_page.html", context={"message": arrayToReturn, "theme": theme})
        return render(request, "mainSite/showThems.html", context={"message": arrayToReturn, "theme": theme})


class Top_News_view(APIView):

    def get(self, request):
        """news = []
        gn = GN(lang='ru')
        top = gn.top_news()
        for toper in top["entries"]:
            print(toper["title"])
            print((list(toper["links"])[0])["href"])
            print()

            item = News()

            description_of_article = [toper["title"]]
            title_of_article = [toper["title"]]

            tone = test_tweet(str(title_of_article))
            tone2 = test_tweet(str(description_of_article))
            tone3 = test_tweet(str(all_of_article))
            tone4 = test_article_better(str(title_of_article), str(description_of_article))
            tone5 = test_article_the_best_api(str(title_of_article), str(description_of_article))

            item.title = title_of_article[0]
            item.body = description_of_article[0]
            item.url = (list(toper["links"])[0])["href"]
            item.rating = tone5

            news.append(item)

        serializer = NewsSerializer(news, many=True)
        return Response({"status": "ok", "news": serializer.data})"""

        news = []

        arrayToReturn = []
        articleTitleArray = ''
        articleLinkArray = ''

        gn = GN(lang='ru')
        top = gn.top_news()
        for toper in top["entries"]:
            print(toper["title"])
            print((list(toper["links"])[0])["href"])
            print()

            item = News()

            articleTitleArray += toper["title"] + '<break>'
            articleLinkArray += (list(toper["links"])[0])["href"] + '<break>'

        print('out of for')
        lemmazAllArticles = myLemm.lemmatize(regex.sub('', articleTitleArray).lower())
        articleTitleArrayLemma = ''.join(lemmazAllArticles)
        articleTitleArray = articleTitleArray.split('<break>')
        print()
        articleTitleArrayLemma = articleTitleArrayLemma.split('<break>')
        articleLinkArray = articleLinkArray.split('<break>')
        print(" size of lemm = " + str(len(articleTitleArrayLemma)))
        for i in range(len(articleTitleArrayLemma)):
            print("articleTitleArray[i]")
            print(articleTitleArray[i])
            tone5 = neuralNetwork.test_article_the_best_api(articleTitleArrayLemma[i], articleTitleArrayLemma[i])

            item = News()

            item.title = articleTitleArray[i]
            item.body = articleTitleArray[i]
            item.url = articleLinkArray[i]
            item.rating = tone5

            news.append(item)

        serializer = NewsSerializer(news, many=True)
        return Response({"status": "ok", "news": serializer.data})


def hello(request):
    return render(request, 'mainSite/index.html', context={})


class NewsView(APIView):

    def get(self, request, theme):
        print(theme)
        news = []
        googlenews = GoogleNews()
        arrayToReturn = []
        articleTitleArray = ''
        articleDescriptionArray = ''
        articleMediaArray = ''
        articleLinkArray = ''
        for site in sites:
            googlenews.clear()
            googlenews = GoogleNews(lang='ru')
            googlenews.search(theme + " " + site)
            googlenews.get_page(PAGE_NUM)
            for result in googlenews.results():
                if sites.__contains__(result['media']):
                    articleTitleArray += result['title'] + '<break>'
                    articleDescriptionArray += result['desc'] + '<break>'
                    articleMediaArray += result['media'] + '<break>'
                    articleLinkArray += result['link'] + '<break>'
        print('out of for')
        lemmazAllArticles = myLemm.lemmatize(
            regex.sub('', articleTitleArray).lower() + "<end>" + regex.sub('', articleDescriptionArray))
        articleTitleArrayLemma, articleDescriptionArrayLemma = (''.join(lemmazAllArticles)).split('<end>')
        articleTitleArray = articleTitleArray.split('<break>')
        articleDescriptionArray = articleDescriptionArray.split('<break>')

        articleDescriptionArrayLemma = articleDescriptionArrayLemma.split('<break>')
        articleTitleArrayLemma = articleTitleArrayLemma.split('<break>')
        articleLinkArray = articleLinkArray.split('<break>')
        countOfArticlse = len(articleTitleArray)

        for i in range(countOfArticlse):
            # проверка на наличие такой же статьи

            flagToBreak = False
            for item in arrayToReturn:
                if articleTitleArray[i] == item["title"]:
                    flagToBreak = True
                    break
            if flagToBreak or articleTitleArray[i] == '\n' : continue

            print(articleTitleArray[i])
            tone5 = neuralNetwork.test_article_the_best_api(str([articleTitleArrayLemma[i]]),
                                                        str([articleDescriptionArrayLemma[i]]))
            # tone6 = neuralNetwork.test_article_the_best_modern(str([articleTitleArrayLemma[i]]),
            #                                                   str([articleDescriptionArrayLemma[i]]))

            item = News()

            item.title = articleTitleArray[i]
            item.body = articleDescriptionArray[i]
            item.url = articleLinkArray[i]
            item.rating = tone5

            news.append(item)
        #print(news)
        serializer = NewsSerializer(news, many=True)
        print(serializer.data)
        return Response({"status": "ok", "news": serializer.data})

        """news = []
        googlenews = GoogleNews(lang='ru')
        for site in sites:
            googlenews.search(theme + " " + site)
            googlenews.get_page(PAGE_NUM)
            for result in googlenews.results():
                item = News()
                description_of_article = [result["desc"]]
                title_of_article = [result["title"]]
                media = result["media"]
                if media != "Lenta" and media != "РИА Новости" and media != "РБК" and media != "Meduza": continue

                flagToBreak = False
                for item in dataa:
                    if title_of_article[0] == item["title"]:
                        flagToBreak = True
                        break
                if flagToBreak: continue

                tone5 = neuralNetwork.test_article_the_best_api(str(title_of_article), str(description_of_article))

                item.title = title_of_article[0]
                item.body = description_of_article[0]
                item.url = result["link"]
                item.rating = tone5

                news.append(item)

            serializer = NewsSerializer(news, many=True)
            return Response({"status": "ok", "news": serializer.data})"""

        def post(self, request):
            article = request.data.get('article')
            # Create an article from the above data
            serializer = NewsSerializer(data=article)
            if serializer.is_valid(raise_exception=True):
                article_saved = serializer.save()
            return Response({"success": "Article '{}' created successfully".format(article_saved.title)})


class NewsViewWithThemes(APIView):

    def get(self, request, theme, pk):
        saved_article = get_object_or_404(Person_with_sites.objects.all(), pk=pk)
        sites_array = saved_article.sites.split(";")
        news = []
        googlenews = GoogleNews()
        arrayToReturn = []
        articleTitleArray = ''
        articleDescriptionArray = ''
        articleMediaArray = ''
        articleLinkArray = ''
        for site in sites_array:
            if not sites_array.__contains__(site):
                continue
            googlenews.clear()
            googlenews = GoogleNews(lang='ru')
            googlenews.search(theme + " " + site)
            for page_num in range(5):
                googlenews.get_page(page_num)
                for result in googlenews.results():
                    if sites_array.__contains__(result['media']):
                        articleTitleArray += result['title'] + '<break>'
                        articleDescriptionArray += result['desc'] + '<break>'
                        articleMediaArray += result['media'] + '<break>'
                        articleLinkArray += result['link'] + '<break>'
        print('out of for')
        lemmazAllArticles = myLemm.lemmatize(
            regex.sub('', articleTitleArray).lower() + "<end>" + regex.sub('', articleDescriptionArray))
        articleTitleArrayLemma, articleDescriptionArrayLemma = (''.join(lemmazAllArticles)).split('<end>')
        articleTitleArray = articleTitleArray.split('<break>')
        articleDescriptionArray = articleDescriptionArray.split('<break>')

        articleDescriptionArrayLemma = articleDescriptionArrayLemma.split('<break>')
        articleTitleArrayLemma = articleTitleArrayLemma.split('<break>')
        articleLinkArray = articleLinkArray.split('<break>')
        countOfArticlse = len(articleTitleArray)

        for i in range(countOfArticlse):
            # проверка на наличие такой же статьи
            flagToBreak = False
            for item in news:
                #print(articleTitleArray[i] + " --- " + item.title)
                if articleTitleArray[i] == item.title:
                    print( articleTitleArray[i] + " --- " + item.title)
                    flagToBreak = True
                    break
            if flagToBreak or articleTitleArray[i] == '' : continue

            #print(articleTitleArray[i])
            tone5 = neuralNetwork.test_article_the_best_api(str([articleTitleArrayLemma[i]]),
                                                        str([articleDescriptionArrayLemma[i]]))
            # tone6 = neuralNetwork.test_article_the_best_modern(str([articleTitleArrayLemma[i]]),
            #                                                   str([articleDescriptionArrayLemma[i]]))

            item = News()

            item.title = articleTitleArray[i]
            item.body = articleDescriptionArray[i]
            item.url = articleLinkArray[i]
            item.rating = tone5

            news.append(item)
        #print(news)
        serializer = NewsSerializer(news, many=True)
        #print(serializer.data)
        return Response({"status": "ok", "news": serializer.data})

        """news = []
        googlenews = GoogleNews(lang='ru')
        for site in sites:
            googlenews.search(theme + " " + site)
            googlenews.get_page(PAGE_NUM)
            for result in googlenews.results():
                item = News()
                description_of_article = [result["desc"]]
                title_of_article = [result["title"]]
                media = result["media"]
                if media != "Lenta" and media != "РИА Новости" and media != "РБК" and media != "Meduza": continue

                flagToBreak = False
                for item in dataa:
                    if title_of_article[0] == item["title"]:
                        flagToBreak = True
                        break
                if flagToBreak: continue

                tone5 = neuralNetwork.test_article_the_best_api(str(title_of_article), str(description_of_article))

                item.title = title_of_article[0]
                item.body = description_of_article[0]
                item.url = result["link"]
                item.rating = tone5

                news.append(item)

            serializer = NewsSerializer(news, many=True)
            return Response({"status": "ok", "news": serializer.data})"""

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
        users = Person_with_sites.objects.all()

        for user in users:
            if user.login == checking_user["login"]:
                found_user_with_login = True
                if user.password == checking_user["password"]:
                    serializer = UserWithSitesSerializer(user)
                    return Response({"status": "ok", "user": serializer.data})

        if found_user_with_login:
            return Response({"status": "bad request", "trouble": "password is incorrect"})
        else:
            return Response({"status": "bad request", "trouble": "no user with such login"})


class UserView(APIView):

    def get(self, request):
        users = Person_with_sites.objects.all()
        serializer = UserWithSitesSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request):
        user_checking = request.data.get("user")
        serializer = UserWithSitesSerializer(data=user_checking)
        serializer.sites = DEFAULT_SITES_FOR_MOBILE
        print(serializer.sites)
        if serializer.is_valid(raise_exception=True):
            users = Person_with_sites.objects.all()
            for user in users:
                if user.login == user_checking["login"]:
                    return Response({"status": "bad response", "trouble": "User with such login is already exists"})

        serializer.save()
        return Response({"status": "ok"})

    def put(self, request, pk):
        saved_article = get_object_or_404(Person_with_sites.objects.all(), pk=pk)
        data = request.data.get('user')
        serializer = UserWithSitesSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "ok", "user": serializer.data
        })

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Person_with_sites.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Person with id `{}` has been deleted.".format(pk)
        }, status=204)
