from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect, StreamingHttpResponse
from Function_modles import img, show_math, excel, aprior
from pro.models import  Data,History
from os import listdir
import os
import xlrd
import shutil
import json
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#主界面
def home(request):
    context = {

    }
    return render(request, 'home.html',context)

#上传图片界面
def index(request):
    if request.method == 'GET':
        context = {
            "upload1": "请先上传图片"
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        files = request.FILES.getlist('fafafa')
        if os.path.isdir(BASE_DIR + '/upload'):
            pass
        else:
            os.mkdir(BASE_DIR + '/upload')
        for file in files:
            f = open(os.path.join(BASE_DIR, 'upload', file.name), 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
        context = {
            "upload1": '上传成功'
        }
        return render(request, 'index.html', context)

#上传文件界面
def index2(request):
    if request.method == 'GET':

        path = 'E:/Notes/python/Project/Django/Show/static/upload'
        if not os.path.exists(path):
            os.mkdir(path)
        L = listdir(path)
        if L == []:
            L = img.ProcessPicture()
            for i in L:
                da = Data(第一大题=i[0], 第二大题=i[1], 第三大题=i[2], 第四大题=i[3], 第五大题=i[4], 总分=i[5])
                da.save()
            show = Data.objects.all()
            context = {
            "upload1": "请先上传表格",
                "show": show
            }
        else:
            show = Data.objects.all()
            context = {
                "upload1": "请先上传表格",
                "show": show
            }
        return render(request, 'index2.html', context)
    elif request.method == 'POST':
        path = 'E:/Notes/python/Project/Django/Show/static/upload'
        if not os.path.exists(path):
            os.mkdir(path)
        L = listdir(path)
        if L == []:
            L = img.ProcessPicture()
            for i in L:
                da = Data(第一大题=i[0], 第二大题=i[1], 第三大题=i[2], 第四大题=i[3], 第五大题=i[4], 总分=i[5])
                da.save()
            show = Data.objects.all()
            context = {
                "upload1": "上传成功",
                "show": show
            }
        else:
            show = Data.objects.all()
            context = {
                "upload1": "上传成功",
                "show": show
            }

        files = request.FILES.getlist('fafa')
        if os.path.isdir(BASE_DIR + '/upload2'):
            pass
        else:
            os.mkdir(BASE_DIR + '/upload2')
        for file in files:
            f = open(os.path.join(BASE_DIR, 'upload2', file.name), 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
        return render(request, 'index2.html', context)

#数据分析界面
def test(request):
    path = 'E:/Notes/python/Project/Django/Show/static/upload'
    if not os.path.exists(path):
        os.mkdir(path)
    L = listdir(path)
    if L == []:
        L = img.ProcessPicture()
        for i in L:
            da = Data(第一大题=i[0], 第二大题=i[1], 第三大题=i[2], 第四大题=i[3], 第五大题=i[4], 总分=i[5])
            da.save()
        show = Data.objects.all()
        data = []
        for one in show:
            data.append(one.总分)

        data_List = excel.getData()[3]
        jigelv, jige = show_math.Jigelv(data_List)
        heigh = show_math.Zuigaofen(data_List)
        balance = show_math.Pingjunfen(data_List)
        each, eachnum = show_math.Fenduan(data_List)
        nandu = show_math.Nandu(data_List)
        qufendu = show_math.Qufendu(data_List)
        weijilv = show_math.Weijilv(data_List)
        xindu = show_math.Xindu(data_List)
        xiaodu = show_math.Xiaodu(data_List)


        outpath = excel.export('localhost', 'root', 'hcwnbs', 'show', 'data')
        path, year, month, day = excel.toSql(outpath)
        hi = History(path=path, year=year, month=month, day=day)
        hi.save()

        know = []
        aprior.processAprior(excel.getData()[1])
        data_dir = r"E:/Notes/python/Project/Django/Show/static/download/aprior.xlsx"
        book = xlrd.open_workbook(data_dir)
        sheet0 = book.sheet_by_index(0)
        nrows = sheet0.nrows
        for i in range(1, nrows):
            cell_value1 = sheet0.cell_value(i, 0)
            cell_value2 = sheet0.cell_value(i, 1)
            know.append([cell_value1, cell_value2])
        for one in know:
            if one[0] == '':
                know.remove(one)
        os.remove(data_dir)
        context = {
            "jigelv": jigelv,
            "jige": jige,
            "heigh": heigh,
            "balance": balance,
            "each": each,
            "eachnum": eachnum,
            "nandu":nandu,
            "qufendu":qufendu,
            "weijilv":weijilv,
            "xindu":xindu,
            "xiaodu":xiaodu,
            "know": know,
            "show": show
        }
        return render(request, 'test.html', context)
    else:
        show = Data.objects.all()
        data = []
        for one in show:
            data.append(one.总分)


        data_List = excel.getData()[3]
        jigelv, jige = show_math.Jigelv(data_List)
        heigh = show_math.Zuigaofen(data_List)
        balance = show_math.Pingjunfen(data_List)
        each, eachnum = show_math.Fenduan(data_List)
        nandu = show_math.Nandu(data_List)
        qufendu = show_math.Qufendu(data_List)
        weijilv = show_math.Weijilv(data_List)
        xindu = show_math.Xindu(data_List)
        xiaodu = show_math.Xiaodu(data_List)

        excel.export('localhost', 'root', 'hcwnbs', 'show', 'data')
        outpath = excel.export('localhost', 'root', 'hcwnbs', 'show', 'data')
        path, year, month, day = excel.toSql(outpath)
        hi = History(path=path, year=year, month=month, day=day)
        hi.save()

        know = []
        aprior.processAprior(excel.getData()[1])
        data_dir = r"E:/Notes/python/Project/Django/Show/static/download/aprior.xlsx"
        book = xlrd.open_workbook(data_dir)
        sheet0 = book.sheet_by_index(0)
        nrows = sheet0.nrows
        for i in range(1, nrows):
            cell_value1 = sheet0.cell_value(i, 0)
            cell_value2 = sheet0.cell_value(i, 1)
            know.append([cell_value1, cell_value2])
        print(know)
        for one in know:
            if one[0] == '':
                know.remove(one)
        os.remove(data_dir)

        context = {
            "jigelv": jigelv,
            "jige": jige,
            "heigh": heigh,
            "balance": balance,
            "each": each,
            "eachnum": eachnum,
            "nandu": nandu,
            "qufendu": qufendu,
            "weijilv": weijilv,
            "xindu": xindu,
            "xiaodu": xiaodu,
            "know": know,
            "show": show
        }
        return render(request, 'test.html', context)

#历史记录界面
def contact(request):

    L = listdir("E:/Notes/python/Project/Django/Show/static/download/")
    context = {
        "name": L[0]
    }

    return render(request, 'contact.html', context)

#报错界面
def services(request):

    show = Data.objects.all()
    context= {
        "show": show
    }

    return render(request, 'services.html', context)

#数据分析界面（如果数据库没有数据）
def inside(request):
    if not os.path.exists('E:/Notes/python/Project/Django/Show/upload'):
        data = Data.objects.all()
        data.delete()
        return render(request, 'inside.html', {"classify": "请先上传图片"})
    else:
        return HttpResponseRedirect('/test')

#下载文件
def download_file(request):

    L = listdir("E:/Notes/python/Project/Django/Show/static/download/")
    the_file_name = L[0]  # 显示在弹出对话框中的默认的下载文件名
    filename = "E:/Notes/python/Project/Django/Show/static/download/" + L[0]  # 要下载的文件路径
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

#处理报错
def processError(request):

    return render(request, "error.html", {"message": "错误提交成功"})

#历史记录搜索功能
def search(request):
    # q = request.GET.get('q')
    # error_msg = ''
    #
    # if not q:
    #     error_msg = '请输入关键词'
    #     return render(request, 'index.html', {'error_msg': error_msg})

    # post_list = Post.objects.filter(title__icontains=q)
    q = request.GET.get('q')
    year = q[:4]
    month = q[5:6]
    day = q[6:8]
    all_list = History.objects.filter(year=year, month=month, day=day)
    download = []
    for i in all_list:
        download.append([i.path, i.path.split('/')[-1]])

    context = {
        "download": download,

    }

    return render(request, 'download.html', context)

#帮助界面
def help(request):
    if not os.path.exists('E:/Notes/python/Project/Django/Show/upload/'):
        os.mkdir('E:/Notes/python/Project/Django/Show/upload/')
    BASE_DIR = 'E:/Notes/python/Project/Django/Show/upload/'
    TO_DIR = 'E:/Notes/python/Project/Django/Show/static/upload/'
    shutil.rmtree(BASE_DIR)
    for i in listdir(TO_DIR):
        os.remove(TO_DIR + i)
    return render(request, 'help.html')