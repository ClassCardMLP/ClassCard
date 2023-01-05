from django.shortcuts import render, redirect
from .models import Card, Benefit, DetailComment, CompareCard
from .forms import DetailCommentForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import random
import json

benefit_all = [
    "혜택2",
    "혜택5",
    "혜택 프로모션",
    "할인",
    "수수료우대",
    "연회비지원",
    "무이자할부",
    "바우처",
    "무실적",
    "모든가맹점",
    "APP",
    "골프",
    "경기관람",
    "레저/스포츠",
    "영화",
    "영화/문화",
    "디지털구독",
    "테마파크",
    "음원사이트",
    "공연/전시",
    "문화센터",
    "게임",
    "고속버스",
    "렌탈",
    "호텔",
    "면세점",
    "리조트",
    "온라인 여행사",
    "여행/숙박",
    "여행사",
    "교통",
    "기차",
    "대중교통",
    "택시",
    "PAYCO",
    "네이버페이",
    "간편결제",
    "카카오페이",
    "삼성페이",
    "차/중고차",
    "충전소",
    "주유",
    "주유소",
    "렌터카",
    "정비",
    "하이패스",
    "자동차",
    "자동차/하이패스",
    "동물병원",
    "펫샵",
    "애완동물",
    "카페",
    "카페/디저트",
    "베이커리",
    "병원",
    "병원/약국",
    "약국",
    "피트니스",
    "드럭스토어",
    "보험",
    "보험사",
    "PAYCO",
    "네이버페이",
    "간편결제",
    "카카오페이",
    "삼성페이",
    "아이스크림",
    "패밀리레스토랑",
    "패스트푸드",
    "저녁",
    "점심",
    "푸드",
    "일반음식점",
    "배달앱",
    "CJ ONE",
    "OK캐쉬백",
    "해피포인트",
    "캐시백",
    "멤버십포인트",
    "적립",
    "BC TOP",
    "SSM",
    "금융",
    "증권사",
    "은행사",
    "KT",
    "LGU+",
    "SKT",
    "통신",
    "헤어",
    "화장품",
    "뷰티/피트니스",
    "대형마트",
    "해외직구",
    "아울렛",
    "홈쇼핑",
    "소셜커머스",
    "쇼핑",
    "백화점",
    "마트/편의점",
    "온라인쇼핑",
    "전통시장",
    "편의점",
    "공항",
    "공항라운지",
    "공항라운지/PP",
    "대한항공",
    "아시아나항공",
    "항공권",
    "항공마일리지",
    "제주항공",
    "저가항공",
    "진에어",
    "라운지키",
    "교육/육아",
    "도서",
    "학습지",
    "학원",
    "어린이집",
    "유치원",
    "SPA브랜드",
    "직장인",
    "비즈니스",
    "프리미엄",
    "프리미엄 서비스",
    "PP",
    "생활",
    "인테리어",
    "아이행복",
    "공과금",
    "공과금/렌탈",
    "국민행복",
    "해외",
    "해외이용",
    "지역",
    "카드사",
    "선택형",
    "하이브리드",
    "제휴/PLCC",
    "기타",
]

# Create your views here.
benefit_dict = {
    "bene": [
        "혜택2",
        "혜택5",
        "혜택 프로모션",
        "할인",
        "수수료우대",
        "연회비지원",
        "무이자할부",
        "바우처",
        "무실적",
        "모든가맹점",
    ],
    "sport": ["골프", "경기관람", "레저/스포츠"],
    "movie": ["영화", "영화/문화", "디지털구독"],
    "culture": ["게임", "테마파크", "음원사이트", "문화센터", "공연/전시"],
    "travel": ["고속버스", "렌탈", "호텔", "면세점", "리조트", "온라인 여행사", "여행/숙박", "여행사"],
    "transport": ["교통", "기차", "대중교통", "택시"],
    "pay": ["PAYCO", "네이버페이", "간편결제", "카카오페이", "삼성페이"],
    "point": ["CJ ONE", "OK캐쉬백", "해피포인트", "캐시백", "멤버십포인트", "적립", "BC TOP", "SSM"],
    "tele": ["KT", "LGU+", "SKT", "통신"],
    "shop": [
        "대형마트",
        "해외직구",
        "아울렛",
        "홈쇼핑",
        "소셜커머스",
        "쇼핑",
        "백화점",
        "마트/편의점",
        "온라인쇼핑",
        "전통시장",
        "편의점",
    ],
    "edu": ["교육/육아", "도서", "학습지", "학원", "어린이집", "유치원"],
    "business": ["직장인", "비즈니스"],
    "life": ["생활", "인테리어", "아이행복"],
    "gov": ["공과금", "공과금/렌탈", "국민행복"],
    "card_bene": ["카드사", "선택형", "하이브리드", "제휴/PLCC"],
    "app": ["APP"],
    "pet": ["동물병원", "펫샵", "애완동물"],
    "car": ["차/중고차", "충전소", "주유", "주유소", "렌터카", "정비", "하이패스", "자동차", "자동차/하이패스"],
    "cafe": ["카페", "카페/디저트", "베이커리"],
    "health": ["병원", "병원/약국", "약국", "피트니스", "드럭스토어"],
    "assurance": ["보험", "보험사"],
    "food": ["아이스크림", "패밀리레스토랑", "패스트푸드", "저녁", "점심", "푸드", "일반음식점", "배달앱"],
    "finance": ["금융", "증권사", "은행사"],
    "beauty": ["헤어", "화장품", "뷰티/피트니스"],
    "airplane": ["공항","공항라운지","공항라운지/PP","대한항공","아시아나항공","항공권","항공마일리지","제주항공","저가항공","진에어","라운지키",],
    "fashion": ["SPA브랜드"],
    "premium": ["프리미엄", "프리미엄 서비스", "PP"],
    "place": ["해외", "해외이용", "지역"],
    "etc": ["기타"],
    "note": ["유의사항"],
}

kor_benefit_dict_keys = ["혜택",    "스포츠",    "영화",    "문화",    "여행",    "교통",    "페이",    "포인트",    "통신사",    "쇼핑",    "교육",    "비즈니스",    "생활",    "공과금",    "카드",    "어플",    "애완동물",    "자동차",    "카페",    "건강",    "보험",    "음식",    "금융",    "뷰티",    "항공",    "패션",    "프리미엄",    "지역",    "기타",    "유의사항"]

benefit_lst = benefit_dict.keys()
benefit_key = list(benefit_lst)


def detail(request, num):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    try:
        card = Card.objects.get(pk=num)
        benefit = Benefit.objects.filter(card_id=num)
        benefit_cate = []
        # benefit과 benfit_cate를 하나씩 튜플로 넣어서 저장하기
        # 탬플렛에서 사용하기 편하게
        bnf_list = []

        for bnf in benefit:

            if bnf.bnf_name in benefit_dict["bene"]:
                benefit_cate.append("혜택")
            elif bnf.bnf_name in benefit_dict["sport"]:
                benefit_cate.append("스포츠")
            elif bnf.bnf_name in benefit_dict["movie"]:
                benefit_cate.append("영화")
            elif bnf.bnf_name in benefit_dict["culture"]:
                benefit_cate.append("문화")
            elif bnf.bnf_name in benefit_dict["travel"]:
                benefit_cate.append("여행")
            elif bnf.bnf_name in benefit_dict["transport"]:
                benefit_cate.append("교통")
            elif bnf.bnf_name in benefit_dict["pay"]:
                benefit_cate.append("페이")
            elif bnf.bnf_name in benefit_dict["point"]:
                benefit_cate.append("포인트")
            elif bnf.bnf_name in benefit_dict["tele"]:
                benefit_cate.append("통신사")
            elif bnf.bnf_name in benefit_dict["shop"]:
                benefit_cate.append("쇼핑")
            elif bnf.bnf_name in benefit_dict["edu"]:
                benefit_cate.append("교육")
            elif bnf.bnf_name in benefit_dict["business"]:
                benefit_cate.append("비즈니스")
            elif bnf.bnf_name in benefit_dict["life"]:
                benefit_cate.append("생활")
            elif bnf.bnf_name in benefit_dict["gov"]:
                benefit_cate.append("공과금")
            elif bnf.bnf_name in benefit_dict["card_bene"]:
                benefit_cate.append("카드")
            elif bnf.bnf_name in benefit_dict["app"]:
                benefit_cate.append("어플")
            elif bnf.bnf_name in benefit_dict["pet"]:
                benefit_cate.append("애완동물")
            elif bnf.bnf_name in benefit_dict["car"]:
                benefit_cate.append("자동차")
            elif bnf.bnf_name in benefit_dict["cafe"]:
                benefit_cate.append("카페")
            elif bnf.bnf_name in benefit_dict["health"]:
                benefit_cate.append("건강")
            elif bnf.bnf_name in benefit_dict["assurance"]:
                benefit_cate.append("보험")
            elif bnf.bnf_name in benefit_dict["food"]:
                benefit_cate.append("음식")
            elif bnf.bnf_name in benefit_dict["finance"]:
                benefit_cate.append("금융")
            elif bnf.bnf_name in benefit_dict["beauty"]:
                benefit_cate.append("뷰티")
            elif bnf.bnf_name in benefit_dict["airplane"]:
                benefit_cate.append("항공")
            elif bnf.bnf_name in benefit_dict["fashion"]:
                benefit_cate.append("패션")
            elif bnf.bnf_name in benefit_dict["premium"]:
                benefit_cate.append("프리미엄")
            elif bnf.bnf_name in benefit_dict["place"]:
                benefit_cate.append("지역")
            elif bnf.bnf_name in benefit_dict["etc"]:
                benefit_cate.append("기타")
            elif bnf.bnf_name in benefit_dict["note"]:
                benefit_cate.append("유의사항")

        for j in range(len(benefit)):
            bnf_list.append((benefit[j], benefit_cate[j]))

        detail_comment_form = DetailCommentForm()

        detail_comments = card.detailcomment_set.filter(card_id=num).order_by("-updated_at")

        detail_comments_num = card.detailcomment_set.filter(card_id=num).count()

        # =============== 카드 비교 ==========
        compare_card = CompareCard.objects.filter(card_id=card.pk)
        user_compare_card = []

        for c in compare_card:
            user_compare_card.append(c.user)

        context = {
            "compare_cards": compare_cards,
            # 카드 배너
            "card_id": card.pk,
            "card_img": card.card_img,
            "card_name": card.card_name,
            # 카드사
            "card_brand": card.card_brand,
            # 국내 해외 전용
            "card_in_out_1": card.card_in_out_1,
            "card_in_out_2": card.card_in_out_2,
            "card_in_out_3": card.card_in_out_3,
            # 전월실적
            "card_record": card.card_record,
            # 연동 해외 카드
            "card_overseas": card.card_overseas,
            # ===== 주요 혜택 ========
            "benefit_count": range(len(benefit)),
            "benefits": bnf_list,
            # ========= 댓글 관련 =======
            "detail_comment_form": detail_comment_form,
            "detail_comments": detail_comments,
            "detail_comments_num": detail_comments_num,
            # CompareCard
            "user_card_compare": user_compare_card,
        }
    except:
        return redirect("main")

    return render(request, "card/detail.html", context)


@login_required(login_url='/login/')
def comment(request, pk):
    card = Card.objects.get(pk=pk)
    user = request.user.pk

    if request.user.is_authenticated:
        if request.method == "POST":
            comment_form = DetailCommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.card = card
                comment.user = request.user
                comment.save()

        comments = DetailComment.objects.filter(card_id=pk).order_by("-updated_at")
        comment_data = []

        for comment in comments:
            comment_data.append(
                {
                    "user_id": comment.user.id,
                    "comment_id": comment.id,
                    "userName": comment.user.username,
                    "rate": comment.rate,
                    "content": comment.content,
                    "update": comment.updated_at,
                }
            )

        data = {
            "commentData": comment_data,
            "user": user,
            "cardId": card.pk,
        }

        return JsonResponse(data)


@login_required(login_url='/login/')
def comment_delete(request, card_id, comment_pk):
    card = Card.objects.get(pk=card_id)
    comment = DetailComment.objects.get(pk=comment_pk)
    user = request.user.pk

    comment.delete()

    comments = DetailComment.objects.filter(card_id=card_id).order_by("-updated_at")
    comment_data = []

    for comment in comments:
        comment_data.append(
            {
                "user_id": comment.user.id,
                "comment_id": comment.id,
                "userName": comment.user.username,
                "rate": comment.rate,
                "content": comment.content,
                "update": comment.updated_at,
            }
        )

    data = {
        "commentData": comment_data,
        "user": user,
        "cardId": card.pk,
    }

    return JsonResponse(data)


@login_required(login_url='/login/')
def comment_update(request, card_id, comment_pk):
    card = Card.objects.get(pk=card_id)
    comment = DetailComment.objects.get(pk=comment_pk)
    user = request.user.pk

    jsonObject = json.loads(request.body)

    if request.method == "POST":
        comment.content = jsonObject.get("content")
        comment.rate = jsonObject.get("rate")
        comment.save()

    comments = DetailComment.objects.filter(card_id=card_id).order_by("-updated_at")
    comment_data = []

    for comment in comments:
        comment_data.append(
            {
                "user_id": comment.user.id,
                "comment_id": comment.id,
                "userName": comment.user.username,
                "rate": comment.rate,
                "content": comment.content,
                "update": comment.updated_at,
            }
        )

    data = {
        "commentData": comment_data,
        "user": user,
        "cardId": card.pk,
    }

    return JsonResponse(data)


from django.core.paginator import Paginator, PageNotAnInteger


card_list = []

@login_required(login_url='/login/')
def search(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = '로그인을 해야 카드 비교 기능을 사용하실 수 있습니다'

    context = {
        "compare_cards" :compare_cards,
        "kor_benefit_lst": kor_benefit_dict_keys,
    }
    return render(request, "card/search.html", context)



def cardcompanylist(request):
    # ======== nav바에 카드비교 카테고리 ========= 
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = '로그인을 해야 카드 비교 기능을 사용하실 수 있습니다'

    context = {
        "compare_cards" : compare_cards,
    }
    return render(request, 'card/cardcompanylist.html', context)


def cardcompany(request,company):

    # ======== nav바에 카드비교 카테고리 ========= 
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = '로그인을 해야 카드 비교 기능을 사용하실 수 있습니다'


    page = request.GET.get('page')
    card_list = Card.objects.filter(card_brand=company)
    paginator = Paginator(card_list, 20)
    cards = paginator.get_page(page)

    context = {
        "compare_cards" : compare_cards,
        'card_list' : cards,

    }
    return render(request,'card/cardcompany.html', context)
    
from django.db.models import Count

@login_required(login_url='/login/')
def bookmark(request,pk):

    user = request.user
    card = Card.objects.get(pk=pk)
    not_work = True
    compare_add = True

    compare_bag = []

    if user.is_authenticated:
        user_bookmark = CompareCard.objects.filter(user = user)
        
        # CompareCard에 해당 유저 내용이 없으면, 바로 유저와 카드를 저장한다
        if len(user_bookmark) == 0:
            compare_add = True
            compare = CompareCard(user=user, card=card)
            compare.save()
        
        else:
            # 유저가 저장한 카드 내용들을 bookmark_card에 저장한다
            bookmark_card = []
            for bookmark in user_bookmark:
                    bookmark_card.append(bookmark.card)

            if 0 < len(bookmark_card) <= 3 :
                # 같은 카드가 있는지 확인하고, 있으면 지워버린다

                if card in bookmark_card:
                    compare_add = False
                    card_ind = bookmark_card.index(card)
                    user_bookmark[card_ind].delete()

                else:
                    # 3개까지 카드를 저장할 수 있다
                    if len(bookmark_card) + 1 != 4:
                        compare_add = True
                        compare = CompareCard(user=user, card=card)
                        compare.save() 
                    else:
                        not_work = False
                        messages.warning(request,'카드 3개까지 추가가 가능합니다! 비교함에서 카드를 꺼내주세요 ㅜ.ㅜ')
                        pass

            else:
                not_work = False
                messages.warning(request,'카드 3개까지 추가가 가능합니다! 비교함에서 카드를 꺼내주세요 ㅜ.ㅜ')
    else:
        pass

    
    cardcard = CompareCard.objects.filter(user=user)

    for card in cardcard:
        compare_bag.append({
            "cardId" : card.card.id,
            "cardName": card.card.card_name,
            "cardImg": card.card.card_img,
        })

    data = {
        "compareBag" : compare_bag,
        "compareAdd" : compare_add,
        "notWork" : not_work,
    }

    return JsonResponse(data)

card_list = []
def card_list(request):
    # ======== nav바에 카드비교 카테고리 ========= 
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = '로그인을 해야 카드 비교 기능을 사용하실 수 있습니다'

    if request.method == "GET":
        answers_page = request.GET.getlist("answers")

        answers_pages = []
        for an in answers_page:
            answers_pages.append(f'&answers={an}')

    global card_list

    if request.method == "GET":
        card_list = []
        card_brand = []
        cards = Card.objects.exclude(card_name=None).order_by('-pk')

        # ============================ 체크 카드랑 신용카드 분리 하기 ===========================

        check_card = []
        credit_card = []

        for card in cards:
            if "체크" in card.card_name:
                check_card.append(card)
            else:
                credit_card.append(card)

        # ==========================================================

        age = request.GET.get("age", "")
        card_type = request.GET.get("type", "")
        # korean benefit list
        kbl = request.GET.getlist("answers", "")
        brand = request.GET.get("brand", "")

        # ============================ 나이와 카드 종류로 필터링 하기 ==========================================
        if age == "20대":
            age_20 = ["혜택2", "혜택5", "혜택 프로모션", "할인", "수수료우대", "연회비지원", "무이자할부", "바우처", "무실적", "모든가맹점", "APP", "골프", "경기관람", "레저/스포츠", "영화", "영화/문화", "디지털구독", "테마파크", "음원사이트", "공연/전시", "게임", "고속버스", "렌탈", "면세점", "온라인 여행사", "여행/숙박", "여행사", "교통", "기차", "대중교통", "PAYCO", "네이버페이", "간편결제", "카카오페이", "삼성페이", "동물병원", "펫샵", "애완동물", "카페", "카페/디저트", "베이커리", "피트니스", "PAYCO", "네이버페이", "간편결제", "카카오페이", "삼성페이", "아이스크림", "패스트푸드", "저녁", "점심", "푸드", "일반음식점", "배달앱", "CJ ONE", "OK캐쉬백", "해피포인트", "캐시백", "멤버십포인트", "적립", "BC TOP", "SSM", "KT", "LGU+", "SKT", "통신", "헤어", "화장품", "뷰티/피트니스", "해외직구", "아울렛", "소셜커머스", "쇼핑", "백화점", "마트/편의점", "온라인쇼핑", "편의점", "공항", "대한항공", "아시아나항공", "항공권", "항공마일리지", "제주항공", "저가항공", "진에어", "도서", "SPA브랜드", "직장인", "비즈니스", "해외", "해외이용", "지역", "카드사", "선택형", "하이브리드", "제휴/PLCC", "기타"]

            # ================ 카드 혜택 필터링도 입력 했을 때 ==================
            if kbl:
                bnf_list = []

                for k in kbl:
                    bene_index = kor_benefit_dict_keys.index(k)
                    bnfs = benefit_dict[benefit_key[bene_index]]

                    for bnf in bnfs:
                        if bnf in age_20:
                            bnf_list.append(bnf)

                if card_type == "체크":
                    for check in check_card:
                        benefits_temp = Benefit.objects.filter(card_id=check.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(check.card_brand)
                                card_list.append(check)
                                break

                else:
                    for credit in credit_card:
                        benefits_temp = Benefit.objects.filter(card_id=credit.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(credit.card_brand)
                                card_list.append(credit)
                                break


        elif age == "30대":
            age_30 = ["혜택2", "혜택5", "혜택 프로모션", "할인", "수수료우대", "연회비지원", "무이자할부", "바우처", "무실적", "모든가맹점", "APP", "골프", "경기관람", "레저/스포츠", "영화", "영화/문화", "디지털구독", "음원사이트", "공연/전시", "렌탈", "호텔", "면세점", "리조트", "온라인 여행사", "여행/숙박", "여행사", "교통", "기차", "대중교통", "택시", "PAYCO", "네이버페이", "간편결제", "카카오페이", "삼성페이", "차/중고차", "충전소", "주유", "주유소", "렌터카", "정비", "하이패스", "자동차", "자동차/하이패스", "동물병원", "펫샵", "애완동물", "카페", "카페/디저트", "베이커리", "병원", "병원/약국", "약국", "피트니스", "드럭스토어", "보험", "보험사", "PAYCO", "네이버페이", "간편결제", "카카오페이", "삼성페이", "아이스크림", "패밀리레스토랑", "저녁", "점심", "푸드", "일반음식점", "배달앱", "CJ ONE", "OK캐쉬백", "해피포인트", "캐시백", "멤버십포인트", "적립", "BC TOP", "SSM", "금융", "증권사", "은행사", "KT", "LGU+", "SKT", "통신", "헤어", "화장품", "뷰티/피트니스", "대형마트", "해외직구", "아울렛", "소셜커머스", "쇼핑", "백화점", "온라인쇼핑", "편의점", "공항", "대한항공", "아시아나항공", "항공권", "항공마일리지", "제주항공", "저가항공", "진에어", "교육/육아", "도서", "학습지", "학원", "어린이집", "유치원", "SPA브랜드", "직장인", "비즈니스", "생활", "인테리어", "아이행복", "공과금", "공과금/렌탈", "국민행복", "해외", "해외이용", "지역", "카드사", "선택형", "하이브리드", "제휴/PLCC", "기타"]

            # ================ 카드 혜택 필터링도 입력 했을 때 ==================
            if kbl:
                bnf_list = []

                for k in kbl:
                    bene_index = kor_benefit_dict_keys.index(k)
                    bnfs = benefit_dict[benefit_key[bene_index]]

                    for bnf in bnfs:
                        if bnf in age_30:
                            bnf_list.append(bnf)

                if card_type == "체크":
                    for check in check_card:
                        benefits_temp = Benefit.objects.filter(card_id=check.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(check.card_brand)
                                card_list.append(check)
                                break

                else:
                    for credit in credit_card:
                        benefits_temp = Benefit.objects.filter(card_id=credit.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(credit.card_brand)
                                card_list.append(credit)
                                break

        else:
            age_40 = ["혜택2",  "혜택5",  "혜택 프로모션",  "할인",  "수수료우대",  "연회비지원",  "무이자할부",  "바우처",  "무실적",  "모든가맹점",  "APP",  "골프",  "경기관람",  "레저/스포츠", "영화",  "영화/문화",  "디지털구독", "음원사이트",  "공연/전시",  "문화센터",  "렌탈",  "호텔",  "면세점",  "리조트",  "온라인 여행사",  "여행/숙박",  "여행사",  "교통",  "기차",  "대중교통",  "택시",  "PAYCO",  "네이버페이",  "간편결제",  "카카오페이",  "삼성페이",  "차/중고차",  "충전소",  "주유",  "주유소",  "렌터카",  "정비",  "하이패스",  "자동차",  "자동차/하이패스",  "동물병원",  "펫샵",  "애완동물",  "베이커리",  "병원",  "병원/약국",  "약국",  "피트니스",  "드럭스토어",  "보험",  "보험사",  "PAYCO",  "네이버페이",  "간편결제",  "카카오페이",  "삼성페이",  "아이스크림",  "패밀리레스토랑",  "저녁",  "점심",  "푸드",  "일반음식점",  "CJ ONE",  "OK캐쉬백",  "해피포인트",  "캐시백",  "멤버십포인트",  "적립",  "BC TOP",  "SSM",  "금융",  "증권사",  "은행사",  "KT",  "LGU+",  "SKT",  "통신",  "헤어",  "화장품",  "뷰티/피트니스",  "대형마트",  "아울렛",  "홈쇼핑",  "쇼핑",  "백화점",  "온라인쇼핑",  "전통시장",  "편의점",  "공항",  "공항라운지",  "공항라운지/PP",  "대한항공",  "아시아나항공",  "항공권",  "항공마일리지",  "제주항공",  "저가항공",  "진에어",  "라운지키",  "교육/육아",  "도서",  "학습지",  "학원",  "어린이집",  "유치원",  "SPA브랜드",  "직장인",  "비즈니스",  "프리미엄",  "프리미엄 서비스",  "PP",  "생활",  "인테리어",  "아이행복",  "공과금",  "공과금/렌탈",  "국민행복",  "해외",  "해외이용",  "지역",  "카드사",  "선택형",  "하이브리드",  "제휴/PLCC",  "기타"]
            # ================ 카드 혜택 필터링도 입력 했을 때 ==================
            if kbl:
                bnf_list = []

                for k in kbl:
                    bene_index = kor_benefit_dict_keys.index(k)
                    bnfs = benefit_dict[benefit_key[bene_index]]

                    for bnf in bnfs:
                        if bnf in age_40:
                            bnf_list.append(bnf)

                if card_type == "체크":
                    for check in check_card:
                        benefits_temp = Benefit.objects.filter(card_id=check.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(check.card_brand)
                                card_list.append(check)
                                break

                else:
                    for credit in credit_card:
                        benefits_temp = Benefit.objects.filter(card_id=credit.pk)

                        for benefit in benefits_temp:
                            if benefit.bnf_name in bnf_list:
                                card_brand.append(credit.card_brand)
                                card_list.append(credit)
                                break


    # ========== arrange ========
    card_brand = set(card_brand)

    print(card_brand)
        
    if brand != "":
        brand_cate = []
        for card in card_list:
            if card.card_brand == brand:
                brand_cate.append(card)
        card_list = brand_cate
        


    page = int(request.GET.get("p", 1))
    pagenator = Paginator(card_list, 10)
    boards = pagenator.get_page(page)


    context = {
        "compare_cards" : compare_cards,
        "answers_page" : ''.join(answers_pages),
        "card_brand" : card_brand,
        "brand" : brand,
        "card_lst" : boards,
        "age_param": age,
        "card_type_param": card_type, 
    }
    return render(request, "card/card_list.html", context)


@login_required(login_url='/login/')
def card_compare(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    context = {
        "compare_cards": compare_cards,
    }
    return render(request, "card/card_compare.html", context)


def search_list(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    # 혜택 갯수 조절
    air_mileage = Benefit.objects.filter(bnf_name__icontains='항공').values_list("card_id",flat=True).distinct()
    air_mileage = air_mileage.order_by('?')[:6]
    air_mileage_cards = Card.objects.filter(id__in=air_mileage)
    # print(air_mileage_cards)
    # 점심+교통
    luntra = Benefit.objects.filter(bnf_name__in=['점심','교통', '기차', '대중교통', '택시']).values_list("card_id",flat=True).distinct()
    luntra = luntra.order_by('?')[:6]
    luntra_cards = Card.objects.filter(id__in=luntra)
    # print(luntra_cards)
    # 편의점 + 카페
    concafe = Benefit.objects.filter(bnf_name__in=['편의점', '마트/편의점','카페', '카페/디저트', '베이커리']).values_list("card_id",flat=True).distinct()
    concafe = concafe.order_by('?')[:6]
    concafe_cards = Card.objects.filter(id__in=concafe)
    
    # 통신+공과금
    telefee = Benefit.objects.filter(bnf_name__in=['통신','KT', 'LGU+', 'SKT','공과금', '공과금/렌탈']).values_list("card_id",flat=True).distinct()
    telefee = telefee.order_by('?')[:6]
    telefee_cards = Card.objects.filter(id__in=telefee)
    

    # 영화+경기관람
    martedu = Benefit.objects.filter(bnf_name__in=['영화', '영화/문화', '디지털구독','경기관람', '골프']).values_list("card_id",flat=True).distinct()
    martedu = martedu.order_by('?')[:6]
    martedu_cards = Card.objects.filter(id__in=martedu)
    print(martedu)
    
    context = {
        "compare_cards": compare_cards,
        "air_mileage_cards": air_mileage_cards,
        "luntra_cards" : luntra_cards,
        "concafe_cards" : concafe_cards,
        "telefee_cards" : telefee_cards,
        "martedu_cards" : martedu_cards,
    }
    return render(request, "card/search_list.html", context)


def rank(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    page = request.GET.get("page")
    card_credit = Card.objects.filter(card_name__icontains="신용")[:9]
    card_check = Card.objects.filter(card_name__icontains="체크")[:9]
    credit_paginator = Paginator(card_credit, 8)
    check_paginator = Paginator(card_check, 8)
    card_credit_page = credit_paginator.get_page(page)
    card_check_page = check_paginator.get_page(page)
    context = {
        "compare_cards": compare_cards,
        "card_credit": card_credit,
        "card_check": card_check,
        "card_credit_page": card_credit_page,
        "card_check_page": card_check_page,
    }
    return render(request, "card/rank.html", context)
