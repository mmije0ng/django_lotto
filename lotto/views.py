from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import GuessNumbers
from .forms import PostForm

# request 속성: urls.py의 urlpatterns의 url을 인자로 받아들임
def index(request):
    lottos = GuessNumbers.objects.all() # GuessNumbers 테이블의 모든 행(데이터)들을 불러옴
    
    # templates/lotto/default.html 파일
    # lottos 라는 key의 lottos value를 html 파일에 넘겨줌
    return render(request, 'lotto/default.html', {'lottos': lottos}) # context-dict

def post(request): 
    # POST 요청일시 데이터 저장
    if request.method == 'POST':
        print('lotto/new request method: ' + request.method)

        print(request.POST)
        print(request.POST['csrfmiddlewaretoken']+'\n')
        print(request.POST['name']+'\n')
        print(request.POST['text']+'\n')

        form = PostForm(request.POST) # filled form
        print(form)

        # 채워진 양식을 검사하여 유효하다면
        if form.is_valid():
            # 사용자로부터 입력받은 form 데이터에서 추가로 수정해주려는 사항이 있을 경우 save를 보류함
            lotto = form.save(commit = False) # 최종 DB 저장은 아래 generate 함수 내부의 .save()로 처리
            
            print(type(lotto)) # <class 'lotto.models.GuessNumbers'>
            print(lotto)
            lotto.generate()
            
            return redirect('index') # urls.py의 name='index'에 해당

    # GET 요청일시 form에서 데이터를 입력받도록
    # forms.py의 form을 html 파일에 넘겨 폼을 입력받는 화면 생성
    else:
        form = PostForm() # empty form
        return render(request, "lotto/form.html", {"form": form})

def detail(request, lottokey):
    lotto = GuessNumbers.objects.get(pk=lottokey) # lottokey(pk) 값의 데이터 가져오기
    
    return render(request, 'lotto/detail.html', {'lotto': lotto}) # 하나의 데이터(행)을 보여줌

def hello(request):
    return HttpResponse("<h1 style='color:red;'>Hello, world!</h1>")
