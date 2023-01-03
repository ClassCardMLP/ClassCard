from django.shortcuts import render, redirect, get_object_or_404
from .models import Magazine, Comment, Reply
from .forms import MagazineForm, MagazineCommentForm, ReplyCommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from card.models import Card, CompareCard, Benefit
import json

# Create your views here.


def index(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    # 인덱스에서 별점 평균 어떻게 산출할까요 나중에 데이터 넣고 고민해봅시다.
    magazines = Magazine.objects.all()
    mz_year = Magazine.objects.filter(tag__contains="YEAR")
    mz_news = Magazine.objects.filter(tag__contains="NEWS")
    mz_recommend = Magazine.objects.filter(tag__contains="RECOMMEND")
    mz_basic = Magazine.objects.filter(tag__contains="BASIC")
    mz_bodo = Magazine.objects.filter(tag__contains="BODO")
    context = {
        "compare_cards": compare_cards,
        "magazines": magazines,
        "mz_year": mz_year,
        "mz_news": mz_news,
        "mz_recommend": mz_recommend,
        "mz_basic": mz_basic,
        "mz_bodo": mz_bodo,
    }
    return render(request, "magazine/index.html", context)


# admin에서 사용자들 -> 사용자 이름 클릭 -> role 변경(필수항목 점검)
@login_required(login_url="/login/")
def create_(request):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    if request.user.role == "C":
        if request.method == "POST":
            form = MagazineForm(request.POST, request.FILES)
            if form.is_valid():
                magazine_form = form.save(commit=False)
                magazine_form.user = request.user
                magazine_form.save()
                return redirect("magazine:index")
        else:
            form = MagazineForm()
        context = {
            "compare_cards": compare_cards,
            "magazine_form": form,
        }
        return render(request, "magazine/create.html", context)
    else:
        messages.warning(request, "쓰기 권한이 없습니다.")
        return redirect("magazine:index")


def detail(request, pk):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    magazine = Magazine.objects.get(pk=pk)
    mzcomment_form = MagazineCommentForm()
    reply_comment_form = ReplyCommentForm()
    mzcomments = magazine.comment_set.all().order_by("-created_at")

    
    context = {
        "compare_cards": compare_cards,
        "magazine": magazine,
        "mzcomment_form": mzcomment_form,
        "mzcomments": mzcomments,
        "reply_comment": reply_comment_form,
    }
    return render(request, "magazine/detail.html", context)


@login_required(login_url="/login/")
def update_(request, pk):
    # ======== nav바에 카드비교 카테고리 =========
    if request.user.is_authenticated:
        compare_cards = CompareCard.objects.filter(user=request.user)
    else:
        compare_cards = "로그인을 해야 카드 비교 기능을 사용하실 수 있습니다"

    magazine = Magazine.objects.get(pk=pk)
    if request.method == "POST":
        magazine_form = MagazineForm(request.POST, request.FILES, instance=magazine)
        if magazine_form.is_valid():
            form = magazine_form.save(commit=False)
            if request.user == form.user:
                form.save()
            else:
                messages.warning(request,'작성자가 아닙니다!')
            return redirect("magazine:detail", pk)
    else:
        magazine_form = MagazineForm(instance=magazine)
    context = {
        "compare_cards": compare_cards,
        "magazine_form": magazine_form,
    }
    return render(request, "magazine/create.html", context)


@login_required(login_url="/login/")
def delete_magazine(request, pk):
    magazine = Magazine.objects.get(pk=pk)
    if request.user == magazine.user:
        if request.method == "POST":
            magazine.delete()
            return redirect("magazine:index")
        else:
            messages.warning(request, "비정상적인 접근")
            return redirect("magazine:detail", pk)
    else:
        messages.warning(request, "작성자만 삭제 가능")
        return redirect("magazine:detail", pk)


@login_required(login_url="/login/")
def mzcomment_create(request, pk):
    magazine = Magazine.objects.get(pk = pk)
    user = request.user.pk

    if request.method == "POST":
        form = MagazineCommentForm(request.POST)
        if form.is_valid():
            mzcomment_form = form.save(commit=False)
            mzcomment_form.magazine = magazine
            mzcomment_form.user = request.user
            mzcomment_form.save()

    comments = Comment.objects.filter(magazine_id = pk).order_by("-created_at")
    comment_data = []
    reply_data = []

    for comment in comments:
        comment_data.append(
            {
                "user_id": comment.user.id,
                "comment_id": comment.id,
                "userName": comment.user.username,
                "grade": comment.grade,
                "content": comment.content,
                "create": comment.created_at,
            }
        )

        if comment.reply_set.all().count() != 0:
            reply_cnt = comment.reply_set.all().count()
            i = 0
            recomment =[]
            while i != reply_cnt:
                reply = comment.reply_set.all()[i]
                recomment.append({
                    "reply_id" : reply.id,
                    "reply_user_id" : reply.user.id,
                    "reply_comment_id" : reply.comment.id,
                    "reply_user" : reply.user.username,
                    "reply_content" : reply.content,
                    "reply_created" : reply.created_at,
                })
                i += 1
                
            reply_data.append(recomment)
        else:
            reply_data.append([])

    data = {
        "replyData" : reply_data,
        "commentData": comment_data,
        "user": user,
        "mzId": magazine.pk,
    }    

    return JsonResponse(data)


@login_required(login_url="/login/")
def mzcomment_delete(request, mz_pk, mzcm_pk):
    magazine = Magazine.objects.get(pk=mz_pk)
    mzcomment = Comment.objects.get(pk=mzcm_pk)
    user = request.user.pk

    if request.user == mzcomment.user:
        mzcomment.magazine = magazine
        mzcomment.delete()

    comments = Comment.objects.filter(magazine_id = mz_pk).order_by("-created_at")
    comment_data = []
    reply_data = []

    for comment in comments:
        comment_data.append(
            {
                "user_id": comment.user.id,
                "comment_id": comment.id,
                "userName": comment.user.username,
                "grade": comment.grade,
                "content": comment.content,
                "create": comment.created_at,
            }
        )

        if comment.reply_set.all().count() != 0:
            reply_cnt = comment.reply_set.all().count()
            i = 0
            recomment =[]
            while i != reply_cnt:
                reply = comment.reply_set.all()[i]
                recomment.append({
                    "reply_id" : reply.id,
                    "reply_user_id" : reply.user.id,
                    "reply_comment_id" : reply.comment.id,
                    "reply_user" : reply.user.username,
                    "reply_content" : reply.content,
                    "reply_created" : reply.created_at,
                })
                i += 1
                
            reply_data.append(recomment)
        else:
            reply_data.append([])

    data = {
        "replyData" : reply_data,
        "commentData": comment_data,
        "user": user,
        "mzId": magazine.pk,
    }    

    return JsonResponse(data)

def mzcomment_update(request, mz_pk, mzcm_pk):
    magazine = Magazine.objects.get(pk=mz_pk)
    mzcomment = Comment.objects.get(pk=mzcm_pk)
    user = request.user.pk

    jsonObject = json.loads(request.body)

    if request.method == "POST":
        mzcomment.content = jsonObject.get("content")
        mzcomment.grade = jsonObject.get("grade")
        mzcomment.save()

    comments = Comment.objects.filter(magazine_id = mz_pk).order_by("-created_at")
    comment_data = []
    reply_data = []

    for comment in comments:
        comment_data.append(
            {
                "user_id": comment.user.id,
                "comment_id": comment.id,
                "userName": comment.user.username,
                "grade": comment.grade,
                "content": comment.content,
                "create": comment.created_at,
            }
        )

        if comment.reply_set.all().count() != 0:
            reply_cnt = comment.reply_set.all().count()
            i = 0
            recomment =[]
            while i != reply_cnt:
                reply = comment.reply_set.all()[i]
                recomment.append({
                    "reply_id" : reply.id,
                    "reply_user_id" : reply.user.id,
                    "reply_comment_id" : reply.comment.id,
                    "reply_user" : reply.user.username,
                    "reply_content" : reply.content,
                    "reply_created" : reply.created_at,
                })
                i += 1
                
            reply_data.append(recomment)
        else:
            reply_data.append([])

    print(reply_data)

    data = {
        "replyData" : reply_data,
        "commentData": comment_data,
        "user": user,
        "mzId": magazine.pk,
    }  

    return JsonResponse(data)

def reply_create(request, mz_pk, mzcm_pk):
    magazine = Magazine.objects.get(pk=mz_pk)
    mzcomment = Comment.objects.get(pk=mzcm_pk)
    comment = mzcomment.id
    user = request.user.pk

    if request.method == "POST":
        reply_form = ReplyCommentForm(request.POST)
        if reply_form.is_valid():
            mzreply_form = reply_form.save(commit=False)
            mzreply_form.magazine = magazine
            mzreply_form.comment = mzcomment
            mzreply_form.user = request.user
            mzreply_form.save()

    replies = Reply.objects.filter(comment_id = mzcm_pk)

    reply_data = []

    for reply in replies:

        reply_data.append({
            "reply_id" : reply.id,
            "reply_user_id" : reply.user.id,
            "reply_comment_id" : reply.comment.id,
            "reply_user" : reply.user.username,
            "reply_content" : reply.content,
            "reply_created" : reply.created_at,
        })
        

    data = {
        "replyData" : reply_data,
        "user": user,
        "comment" : comment,
        "mzId": magazine.pk,
    }  

    return JsonResponse(data)

def reply_delete(request, mz_pk, mzcm_pk, mzreply_pk):
    magazine = Magazine.objects.get(pk=mz_pk)
    mzcomment = Comment.objects.get(pk=mzcm_pk)
    comment = mzcomment.id
    reply = Reply.objects.get(pk = mzreply_pk)
    user = request.user.pk

    if request.user == reply.user:
        reply.delete()


    replies = Reply.objects.filter(comment_id = mzcm_pk)

    reply_data = []

    for reply in replies:

        reply_data.append({
            "reply_id" : reply.id,
            "reply_user_id" : reply.user.id,
            "reply_comment_id" : reply.comment.id,
            "reply_user" : reply.user.username,
            "reply_content" : reply.content,
            "reply_created" : reply.created_at,
        })
        

    data = {
        "replyData" : reply_data,
        "user": user,
        "comment" : comment,
        "mzId": magazine.pk,
    }  

    return JsonResponse(data)


def magazine_bookmark(request, mz_pk):
    magazine = get_object_or_404(Magazine, pk=mz_pk)

    if not request.user.is_authenticated:
        messages.warning(request, "로그인이 필요합니다.")
        return redirect("/login")

    if magazine.bookmark_users.filter(pk=request.user.pk).exists():
        magazine.bookmark_users.remove(request.user)
        is_bookmarked = False
        # print(is_bookmarked)
    else:
        magazine.bookmark_users.add(request.user)
        is_bookmarked = True
        # print(is_bookmarked)
    # print(magazine.bookmark_users.all())
    context = {
        "is_bookmarked": is_bookmarked,
    }
    return JsonResponse(context)
    # return redirect('magazine:detail', mz_pk)
