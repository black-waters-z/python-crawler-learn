#Flask学习
##Flask基础
```cython
import json
from flask import Flask,render_template,request
import requests
from werkzeug.routing import BaseConverter #导入转换器的基类，用于继承方法
app=Flask(__name__)
```
最基础的flask使用，接下来，我们将一步步深入细化学习
```cython
from flask import Flask
app=Flask(__name__)
@app.route("/")
def index():
    return "hello world"

app.run()
```

路由route的创建  
通过路由在url内添加参数，其关联的函数可以接受该参数
```cython
@app.route("/index/<int:id>",)
def index(id):
    if id==1:
        return 'first'
    if id==2:
        return 'second'
    if id==3:
        return 'third'
    else:
        return 'Hello World'

if __name__=='__main__':
    app.run()
```

除了原有的转换器，我可以自定义转换器pip install werkzeug
```cython
class RegexConverter(BaseConverter):
    def __init__(self,url_map,regex):
        super(RegexConverter,self).__init__(url_map)
        self.regex=regex

    def to_python(self, value):
        # 访问成功时被调用
        print("to_python方法被调用")
        return value

# 将自定义的转换器类添加到flask应用中
app.url_map.converters['re']=RegexConverter

@app.route("/index/<re('1\d{10}'):value>")
def index(value):
    # 在控制台中打印
    print(value)
    return "hello world"

if __name__=='__main__':
    app.run(debug=True)
```

endpoint的作用：  
1.endpoint默认为视图函数的名称  
2.当每个app中都存在一个url_map,这个url_mao中包含了url到endpoint的映射。  
在路由中修改endpoint，相当于为视图函数起别名  
3.endpoint相当于给url起一个名字，view_functions内存储的就是url的名字到视图函数的映射，且endpoint在同一个蓝图下也不能重名

```cython
@app.route('/hello',endpoint='our_set')
def hell_world():
    return "hello world"

if __name__=='__main__':
    print(app.view_functions)
    print(app.url_map)
    app.run(debug=True)
```

request对象的使用  
render_template():可以用于呈现一个我们编写的html文件模板  
request.method:用于获取url接收到的请求方式，以此返回不同的响应页面  

```cython
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method=='POST':
        name=request.form.get('name')
        password=request.form.get('password')
        return name+" "+password

if __name__=="__main__":
    app.run()
```

###请求钩子before/after_request
1.before_request 在每次请求之前，可以执行某个特定功能的函数，先绑定先执行  
2.before_first_request 只在第一次请求之前调用，先绑定的先执行  
3.after_request 每次请求之后都会被调用，先绑定的后执行  
4.teardown_request 每一次请求之后都会调用，先绑定的后执行  

```cython
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.before_request
def before_request_a():
    print('I am in before_request_a')

@app.before_request
def before_request_b():
    print('I am in before_request_b')

if __name__ == '__main__':
    app.run()

```

###redirect重定向
flask.redirect(location,code=302)  
location:需要重定向的url，应该搭配url_for函数来使用  
code表示采用哪个重定向，默认302，即临时性重定向，301永久性重定向  
```cython
from flask import redirect,url_for

@app.route('/index')
def index():
    return redirect(url_for('hello'))

@app.route('/hello')
def hello():
    return 'this is hello fun'

# 效果：输入/index自动跳转到hello
if __name__=='__main__':
    app.run()
```

###返回json数据给前端
方法一：make_response和json库共同完成  
方法二：jsonify库实现，减少代码行数  
```cython
from flask import make_response,json
@app.route("/index")
def index():
    data = {
        'name':'张三'
    }
    response=make_response(json.dumps(data,ensure_ascii=False))
    response.mimetype='application/json'
    return response
# 效果：页面打印出字典

if __name__=='__main__':
    app.run()
```

###flask的config
是一个存储了各项配置的字典  
该操作等效于ensure_ascii=False的配置  
主要作用是 禁用 JSON 响应的 ASCII 编码，确保返回的 JSON数据可以正确显示非 ASCII 字符（如中文、日文、Emoji 等）。
```cython
app.config['JSON_AS_ASCII']=False

@app.route('/index')
def index():
    data={
        'name':'张三'
    }
    return jsonify(data)

if __name__=='__main__':
    app.run()

```

###abort函数的使用
类似于python中的raise函数，可以在需要请求的地方抛出错误，并结束该请求
可以使用errorhandler()装饰器来进行异常的捕获和自定义
```cython
from flask import Flask,render_template,request,abort

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'zhangsan' and password == '123456':
            return 'login sucess'
        else:
            # abort的用法类似于python中的raise，在网页中主动抛出错误
            abort(404)
            return None

# 自定义错误处理方法,将404这个error与Python函数绑定
# 当需要抛出404error时，将会访问下面的代码
@app.errorhandler(404)
def handle_404_error(err):
    # return "发生了错误，错误情况是：%s"%err
    # 自定义一个界面
    return render_template('404.html')

if __name__ == '__main__':
    app.run()
```

url_for实现反转
url_for('模块名.视图名'，变量=参数)
视图名:endpoint,url_for只能使用endpoint设置的名字来反转url

##Flask高级视图
###add_url_rule
这是一种函数，通过调用可以替代app.route()用法
用法如下：
app.add_uel_rule(rule='',end='',view_func=func)
```cython
from flask import Flask,url_for
app=Flask(__name__)

@app.route('/',endpoint='index')
def hello_world():
    return 'hello world'

def my_test():
    return '这是测试页面'

app.add_url_rule(rule='/test',endpoint='test',view_func=my_test)

# 请求上下文只有在发送request请求时才会被激活，激活后request对象被设置为全局可访问
# 其内部封装了客户端发出的请求数据报文
# 此处是主动生成一个临时的测试请求上下文
with app.test_request_context():
    print(url_for('test'))

if __name__=='__main__':
    app.run(debug=True)
```

###类视图
视图实现形式：
1.视图函数（前面）

2.类视图（由类来实现）

####标准类视图：
1）定义时需要继承flask的views.View这一基类
2）每个类视图内必须包含一个dispatch_request方法，每当类视图接收到请求时都会执行该方法，返回值的设定和视图函数相同
3）视图函数可以通过@app.route和app.add_url_rule来进行注册（映射到url），但类视图只能通过app.add_url_rule来注册，
注册时view_func不能直接使用类名，需要调用基类中的as_view方法来为自己取一个“视图函数名”

```cython
from flask import Flask,render_template,views

app = Flask(__name__)

# 定义父视图类继承基类View
class Ads(views.View):
    def __init__(self):
        super(Ads, self).__init__()
        # 实例属性
        self.context={
            'ads':'这是对联广告！'
        }

# 定义子视图类继承父类并实现工程
class Index(Ads):
    def dispatch_request(self):
        # 字典传参方式==不定长的关键字传参
        return render_template('class_mould/index.html',**self.context)
class Login(Ads):
    def dispatch_request(self):
        # 字典传参方式==不定长的关键字传参
        return render_template('class_mould/login.html',**self.context)
class Register(Ads):
    def dispatch_request(self):
        # 字典传参方式==不定长的关键字传参
        return render_template('class_mould/register.html',**self.context)

# 注册我们创建的类视图,as_view给类视图起名
app.add_url_rule(rule='/',endpoint='index',view_func=Index.as_view('index'))
app.add_url_rule(rule='/login/',endpoint='login',view_func=Login.as_view('login'))
app.add_url_rule(rule='/register/',endpoint='register',view_func=Register.as_view('register'))

if __name__=='__main__':
    print(app.view_functions)
    app.run(debug=True)

```
index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
这是首页！{{ ads }}
</body>
</html>
```
login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
这是登录页面！{{ ads }}
</body>
</html>
```
register.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
这是注册页面！{{ ads }}
</body>
</html>
```
####方法类视图
Flask提供了另一种类视图flask.views.MethodView(类似于views.View的基类),在其内部编写的函数方法即是http方法的同名小写映射
```cython
from flask import Flask,render_template,request,views

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# 定义LoginView类
class LoginView(views.MethodView):
    # 定义get函数
    def get(self):
        return render_template("index.html")
    # 定义post函数
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")
        if username == 'admin' and password == 'admin':
            return "用户名正确，可以登录！"
        else:
            return "用户名或密码错误，不可以登录！"

# 注册类视图
# 未设置endpoint，则endpoint默认为as_view设置的类视图名,loginview为视图函数名
app.add_url_rule('/login',view_func=LoginView.as_view('loginview'))

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```
登录界面html代码如下：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<!--action中可以指定表单提交的目标url或文件-->
<!--login指向我们给类视图绑定的url：'/login'-->
<form action="login" method="post">
    USERNAME：
    <input type="text" name="username">
    <br>
    PASSWORD：
    <input type="password" name="password">
    <br>
    <!--提交按钮-->
    <input type="submit" name="submit">
</form>
</body>
</html>
```
###装饰器
本质是一个python函数，可以增加额外功能在不改变其他函数代码的情况下，  
其传入参数一般是函数对象(这里推测可以传入多个)，返回值也是一个函数对象

####不含参数的函数使用装饰器
目前下列代码未同网页进行绑定
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# 定义装饰器函数
def user_login(func):
    def inner():
    	# 替代登录操作
        print('登录操作！')
        # 执行传入的函数对象
        func()
    # 此处如果return inner()，那么返回的是inner函数的执行结果
    # 而使用return inner，则返回的是inner函数
    return inner

# 定义新闻页面视图函数news
def news():
    print('这是新闻详情页！')
# 将news函数作为参数传给装饰器函数
show_news=user_login(news)
# 因为user_login返回inner函数，所以show_news()==inner()
show_news()
# 打印出show_news的真实函数名（为inner）
print(show_news.__name__)

if __name__ == '__main__':
    app.run(debug=True)
```
运行结果：
```
登录操作！
这是新闻详情页！
inner
```
####含参数的函数装饰器
可以使用*args，**kwargs来接收参数

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# 定义装饰器函数
def user_login(func):
    # inner函数接收参数
    def inner(*args,**kwargs):
        print('登录操作！')
        # 执行传入函数时使用inner接收到的参数
        func(*args,**kwargs)
    return inner

# 不带参的不受影响
@user_login
def news():
    print(news.__name__)
    print('这是新闻详情页！')
news()

# 带参的定义时预声明接收的参数
@user_login
def news_list(*args):
    # 获取元组args的第一个元素
    page=args[0]
    print(news_list.__name__)
    print('这是新闻列表页的第'+str(page)+'页！')
# 传递给args的元组即为(5,)
news_list(5)

if __name__ == '__main__':
    app.run(debug=True)

```

###蓝图的使用
上述类视图、装饰器分别通过继承、包装的方式减少了单个flask程序文件里重复代码的出现，实现了程序的优化；  
但是这样处理后的文件内，不同功能的代码块（类视图、视图函数）仍然混杂在一起。  
如果要制作一个非常大型的程序项目，这样不仅会让代码阅读变得十分困难，而且不利于后期维护；  
为了解决这一问题，我们需要引入蓝图（flask.Blueprint），用于实现程序功能的模块化；
```python 
from flask import Blueprint
```
####蓝图的导入创建与使用
主路由函数：创建flask对象，并为拓展模块中的蓝图对象提供注册入口
```python
from flask import Flask
from flask学习 import news,products

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello my world !'

# 将对应模块下的蓝图对象注册到app中
app.register_blueprint(news.new_list)
app.register_blueprint(products.product_list)

if __name__ == '__main__':
    app.run(debug=True)
```
导入的模块：  
news.py
```python
from flask import Blueprint

# 实例化蓝图对象，参数一类似于蓝图对象的名称
# 一个app下的蓝图对象不可重名
new_list = Blueprint('news',__name__)

# 蓝图对象的使用和app类似
# 一个蓝图下的视图函数名、endpoint不可重复
@new_list.route('/news')
def new():
    return '这是新闻模块！'
```
product.py
```python
from flask import Blueprint

new_list = Blueprint('products',__name__)

@new_list.route('/products')
def product():
    return '这是产品模块！'
```
####url_prefix蓝图前缀
方案一：

为视图函数添加统一的前缀，这样子在其后追加的路径都会加在url_prefix路径下
```python
from flask import Blueprint

new_list = Blueprint('news',__name__,url_prefix='/index')

@new_list.route('/news')
def new():
    return '这是新闻模块！'
```
方案二：
```
app.register_blueprint(news.new_list,url_prefix='/test')
```
####设置主域名
```
# 当前网站域名设置为example.com，端口号为5000
app.config['SERVER_NAME'] = 'example.com:5000'
```
example.com（此时我们指定了服务器host不再为localhost，而是0.0.0.0）  
此时访问网站服务器时只能通过域名方式：http://example.com:5000/index，使用http://10.240.142.216:5000/index将返回404:
```python
from flask import Flask
import admin

app = Flask(__name__)

# 配置`SERVER_NAME`，设置主域名
app.config['SERVER_NAME'] = 'example.com:5000'
# 注册蓝图，指定了subdomain
app.register_blueprint(admin.bp)

@app.route('/index')
def index():
    return '通过域名访问！'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

```
####subdomain设置子域名
此时访问的域名为：admin.example.com:5000
```python
from flask import Blueprint
bp = Blueprint('admin',__name__,subdomain = 'admin')

@bp.route('/ad')
def admin():
    return 'Admin Page'
```

##jinja2模版引擎（结合html）

###模版导入与使用
####基础用法
Flask通过render_template来实现模板的渲染
```python
from flask import Flask,render_template
```
示例代码如下：
```python
from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def index():
    data={
        'name':'张三',
        'age':18,
        'mylist':[1,2,3,4,5,6,7]
    }
    # 以键值对的形式传参给模板index2.html
    return render_template('index2.html',data=data)

if __name__=='__main__':
    app.run(debug=True)

```
对应的html页面需要以{{ }}的形式使用该变量
注意，html文件应保存在main.py同级的templates文件夹下
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
hello world
<br>
<!-- 对传入变量的使用并显示：在双括号内，和python中用法类似 -->
{{ data }}
<br>
{{ data['name'] }}
<br>
{{ data.name }}
<br>
mylist:{{ data.mylist }}
<br>
mylist[1]:{{ data.mylist[1] }}
<br>
count:{{ data.mylist[1]+data.mylist[2] }}
</body>
</html>
```
如果有多个变量需要传递，我们可以不需要一个一个进行传参，直接使用**locals()替代我们在当前视图函数中定义的所有变量：

html页面使用方法：**{{author}}** **{{title}}**
```python
from flask import Flask,render_template

app = Flask(__name__)

# 给前端模板传参
@app.route("/")
def index():
	title='python键值对'	# 定义键值1
	author='li'			# 定义键值2
    return render_template('index2.html',**locals()) #渲染模型并传值

if __name__ == '__main__':
    app.run()

```

###模板控制语句
jinja2模板引擎中也可使用if和for控制语句，但是语句需要放置在{% %}中；
####if条件判断
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{% if name==1 %}
	<h1>恭喜你抽中了一等奖！</h1>
{% if name==2 %}
	<h1>恭喜你抽中了二等奖！</h1>
{% else %}
	<h1>恭喜你抽中了三等奖！</h1>
{% endif %}
</body>
</html>
```
####for控制循环
```html
{% for 目标 in 对象 %}
	<p>目标</p>
{% endfor %}
```
for循环的内置常量
```
loop.index: 获取当前的索引值 从1开始
loop.index0:获取当前的索引值 从0开始
loop.first: 判断当前是否是第一次迭代, 是返回True否则返回False
loop.last: 判断当前是否是最后一次迭代, 是返回True否则返回False
loop.length: 序列的长度
```
示例代码：
```html
<ul>
{% for item in list %}
	<li>{{ item }}</li>
	<li>当前的索引是：{{ loop.index }}</li>
	<li>当前的索引是：{{ loop.index0 }}</li>
	<li>当前是否是第一次迭代：{{ loop.first }}</li>
	<li>当前是否是最后一次迭代：{{ loop.last }}</li>
	<li>前序列的长度：{{ loop.length }}</li>
</ul>

```
###过滤器使用和自定义
常用过滤器使用方式
1、前端模板内 {{内容|过滤器}}
2.add_template_filter(函数方法名，‘过滤器名’)来自定义过滤器
```python
from flask import Flask
app=Flask(__name__)

# 自定义过滤器
def list_step(li):
    # 返回列表，步长为2
    return li[::2]

# 注册模板过滤器（filter）
# 参数1为该过滤器调用的函数，参数2为在前端中调用该过滤器使用的名称
app.add_template_filter(list_step,'li2')
```
html页面如下
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<!-- 过滤器的使用 -->
<!-- 全大写 -->
{{ 'hello_world' | upper }}
<br>
<!-- 单词首字母大写 -->
{{ 'hello world' | title }}
<br>
<!-- 替换左边的内容为右边的内容 -->
{{ 'hello_world' | replace('hello','hi') }}
<br>
<!-- 调用自定义的过滤器 -->
mylist列表：{{ data.mylist | li2 }}
</body>
</html>
```
也可以把字符串作为过滤器的返回对象，给前端标签如class，id等属性，结合css
```html
<span class="{{ 给过滤器的参数|过滤器名称 }}"></span>
```
###宏的定义、调用、导入
宏的定义是为了将前端模板中需要反复创建的模块变成一个方便调用的“函数”，
这一操作类似于python中创建函数，也可以传参，但不能有返回值；

宏的定义以macro标志开始，以endmacro结束，同样需要在{% %}中进行。
####宏的定义
```html
<!--不带参数的宏定义，就像是定义一个函数-->
{% macro input() %}
<!--宏内执行的操作，生成一个input表单-->
    <label>
        <input type="text" name="username" value="">
        <br>
    </label>
<% endmacro %}

<!--带参数的宏定义-->
{% macro input2(name, value='', type='text', size=30) %}
    <!-- 此处双括号内的参数，指向我们在定义时设定的参数，调用时没有传值就使用设定的默认值 -->
    <label>表单项2：
        <input type="{{ type }}" name="{{ name }}" value="{{ value }}" size="{{ size }}">
        <br>
    </label>
{% endmacro %}
```
####宏的调用
类似于函数调用，未采用关键字传参则需要注意顺序
```html
{{ input1() }}
{{ input2() }}   <!--name不指定， 则name="", 即和value一样也是空-->
{{ input2('username') }}
{{ input2('username', value='cheng', type='password', size=50) }}
```
####宏的导入
```html
{% import 'index3.html' as index3 %}
    <div>
        <p>用户名：{{index3.input2('username')}}</p>
        <p>密码：{{index3.input2('password',type='password')}}</p>
		<p>登录：{{index3.input2('submit',type='submit',value='登录')}}</p>
    </div>

<!--或者另一种-->
{% from 'index3.html' import input2 %}
	<div>
		<p>用户名：{{input2('username')}}</p>
		<p>密码：{{input2('password',type='password')}}</p>
		<p>登录：{{input2('submit',type='submit',value='登录')}}</p>
	</div>
```
###include的使用
include用于在一个模板的指定位置导入另一个模板的内容，区别于宏的调用，include更像从另一个模板“复制+粘贴”

include同样在{% %}中使用，采用语句{% include 模块名 %}，需要注意两点：  
1.include是直接将目标模板中的所有内容直接“copy”在当前位置，所以被导入的模板如果有head和body部分也将被导入过来；  
2.include和import都是在templates这个目录下搜索的，所以使用路径时不需要添加相对路径：上级目录 “ …/ ” 和当前目录 “ ./ ” ；

```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
	<!-- 可以视为子模板1 -->
    {% include "common/header.html" %}
    <div class="content">
        中间的
    </div>
    <!-- 可以视为子模板2 -->
    {% include "common/footer.html" %}
</body>
</html>
```
header.html子模板
```html
<nav>
	<div class="top">
		这是顶部
	</div>
</nav>
```
footer.html
```html
<footer>
	<div class="bottom">
		这是底部
		<!-- 说明：子模板中可以直接使用父模板的变量，不需要其他操作
		因为这一代码是被复制到父模板中去运行的 -->
		author：{{ name }}
	</div>
</footer>
```
后端导入父模板
```python
from flask import Flask,render_template

app = Flask(__name__)

# 运行时直接将子模板需要的参数传给父模板
@app.route("/")
def index():
	name='时生'
    return render_template('include_test.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)
```
###set与with的使用
我们在模板内需要使用到的变量，不仅可以通过后端传参，也可以由我们自己定义，这样更有利于前后端分离的实现；

set——自定义全局变量：由set定义的变量可以在模板内任意一个地方调用，甚至在子模板中也可以使用；
```html
<!-- 定义普通变量并赋值 -->
{% set telephone=1234567890 %}
<!-- 定义列表变量并赋值 -->
{% set lis=[('produce.html','produce'),('index.html','index')] %}

<!-- 调用 -->
{{ telephone }}
{{ lis }}
```
with——自定义局部变量：with定义的变量只能在{% with %}到{% endwith %}这个代码块间使用；
```html
{% with test=60 %}
	{{ test }}
{% endwith %}
```
###加载静态文件
```html
<head>
	<!-- 导入js文件 -->
	<script type="text/javascript" src="{{url_for('static',filename='js/jquery-3.5.1/jquery-3.5.1.js')}}"></script>
	<!-- 导入css文件 -->
	<link rel="stylesheet" href="{{url_for('static',filename='css/car.css')}}">
</head>
<body>
	<!-- 导入图片 -->
	<img alt="" src="{{ url_for('static',filename='image/car.jpg') }}"/>
    <script>
	if(jQuery){
		alert('jQuery已加载！');
	}
	else{
		alert('jQuery未加载！');
	}
</script>
</body>
```
###extends继承模板
在include中，我们对于当前模板需要插入的代码块，可以在其他模板中定义，然后用include导入进来，外部模块是当前模块的补充；
将子模版插入父模版中。

**类似于用子模版在父模版中搭积木**

而在extends中，我们当前的模板则是待装载的代码块，需要我们继承一个框架来搭载这些代码块，这时候就需要extend来导入框架（基类）模块了；
将父模板框架拿来显示子模板

**可以用于显示相同排版的不同内容**
```html
<!DOCTYPE html>
<html lang="en">
<head>
	<!--除了装载部分，其他部分子模板一律安照当前父模板的定义显示-->
    <meta charset="UTF-8">
    <title>
    	<!--标题中子模板内容的装载位置-->
        {% block title %}
        {% endblock %}
        -我的网站
    </title>
</head>
<body>
	<!--主体中子模板内容的装载位置-->
    {% block body %}
        这是基类中的内容
    {% endblock %}
</body>
</html>
```
son1.html
```html
<!--继承的父类模板文件名称-->
{% extends "father.html" %}
<!--插入到父类代码的title区块的内容-->
{% block title %}
    网站首页
{% endblock %}
<!--插入到父类代码的body区块的内容-->
{% block body %}
	<!--保留父模板该block中原本的内容-->
    {{ super() }}
    <h4>这是网站首页的内容！</h4>
{% endblock %}
```
son2.html
```html
<!--继承的父类模板文件名称-->
{% extends "father.html" %}
<!--插入到父类代码的title区块的内容-->
{% block title %}
    产品列表页
{% endblock %}
<!--插入到父类代码的body区块的内容-->
{% block body %}
    <h4>这是产品列表页的内容！</h4>
    取得网页标题的内容:
    <!--调用当前模板中其他block的内容 -->
    <h4>{{ self.title() }}</h4>
{% endblock %}
```
后端导入两个子模板
```python
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/son1')
def son1():
    return render_template('son_1.html')

@app.route('/son2')
def son2():
    return render_template('son_2.html')

if __name__ == '__main__':
    app.run(debug=True)
```
##Flask数据交互
###使用flask处理表单
传统的前端通用表单，需要前后端共同完成操作。  
如下：
```python
from requests import request
# 判断请求方式
if request.method == 'POST':
	# 获取表单中name为username的文本域提交的数据
	name = request.form.get('username')
	# 获取表单中name为password的文本域提交的数据
	password = request.form.get('password')
	return name+" "+password
```
改进的表单操作，引入第三方扩展包：flask-wtf与wtforms，来实现由后端单独完成的表单操作
```
wtforms安装：pip install wtforms
flask-wtf安装：pip install Flask-WTF or pip install flask-wtf
```
wtforms依照功能类别来说wtforms分别由以下几个类别：
```
Forms: 主要用于表单验证、字段定义、HTML生成，并把各种验证流程聚集在一起进行验证。
Fields: 包含各种类型的字段，主要负责渲染(生成HTML文本域)和数据转换。
Validator：主要用于验证用户输入的数据的合法性。比如Length验证器可以用于验证输入数据的长度。
Widgets：html插件，允许使用者在字段中通过该字典自定义html小部件。
Meta：用于使用者自定义wtforms功能（配置），例如csrf功能开启。
Extensions：丰富的扩展库，可以与其他框架结合使用，例如django。
```
Flask-WTF其实是对wtforms的简单集成，也能通过添加动态token令牌的方式，为所有Form表单提供免受CSRF（Cross-site request forgery——跨站请求伪造）攻击的技术支持

启用CSRF保护  
1.定义配置文件
```
# config.py
CSRF_ENABLED = TRUE # 用于开启CSRF保护，但默认状态下都是开启的
SECRET_KEY = 'X1X2X3X4X5' # 用于生成动态令牌的秘钥
```
```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect # 导入CSRFProtect模块
import config # 导入配置文件

app = Flask(__name__)
# 导入配置模块中的配置
app.config.from_object(config)
# 为当前应用程序启用WTF_CSRF保护，并返回一个CSRFProtect对象
csrf = CSRFProtect(app)
```
2.直接通过键值对方式新增配置
```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect # 导入CSRFProtect模块

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADJLAJDLA' # 用于生成动态令牌的秘钥
app.config['CSRF_ENABLED'] = True # 用于开启CSRF保护，但默认状态下都是开启的
# 为当前应用程序启用WTF_CSRF保护，并返回一个CSRFProtect对象
csrf = CSRFProtect(app)
```
3.接下来，我们需要用到flask_wtf 和 wtforms来定义一个支持CSRF保护的后端表单

一般，我们将之定义在一个类中
```python
from flask import Flask,render_template,request
from flask_wtf.csrf import CSRFProtect
# 导入表单基类FlaskForm
from flask_wtf import FlaskForm
# 导入FlaskForm父类的表单字段组件（字符串文本域，密码文本域，提交按钮）
from wtforms import StringField,PasswordField,SubmitField
# 导入FlaskForm父类的表单验证组件（数据不为空，数据是否相同，数据长度）
from wtforms.validators import DataRequired,EqualTo,Length

app = Flask(__name__)
# 配置加密匙，后端为了保护网站加入的验证机制
# 不加会报错：RuntimeError: A secret key is required to use CSRF.
app.config['SECRET_KEY'] = 'ADJLAJDLA'
# app.config['CSRF_ENABLED'] = True # 可以省略
csrf = CSRFProtect(app)

# 定义表单模型类，继承FlaskForm
class Register(FlaskForm):
    # 定义表单中的元素，类似于html的form中定义input标签下的内容
    # label 用于点击后跳转到某一个指定的field框
    # validators 用于接收一个验证操作列表
    # render_kw 用于给表单字段添加属性，各属性以键值对的形式设置
    user_name = StringField(label='用户名:',validators=[DataRequired(message=u'用户名不能为空'),Length(6,16,message='长度位于6~16之间')],render_kw={'placeholder':'输入用户名'})
    # message中存放判断为错误时要返回的信息，EqualTo中第一个参数是要比较的field组件
    password = PasswordField(label='密码:',validators=[DataRequired(message=u'密码不能为空'),EqualTo('password2',message=u'两次输入需相同'),Length(6,16,message='长度位于6~16之间')],render_kw={'placeholder':'输入密码'})
    password2 = PasswordField(label='再次输入密码:', validators=[DataRequired(message=u'密码不能为空'),Length(6,16,message='长度位于6~16之间')],render_kw={'placeholder':'再次输入密码'})
    submit = SubmitField(label='提交')

@app.route('/',methods=['GET','POST'])
def register():
    # 实例化表单对象
    form = Register()
    if request.method == 'GET':
    	# 表单对象发送至前端
        return render_template('register.html',form=form)
    elif request.method == 'POST':
        # form.validate_on_submit() 等价于：request.method=='post' and form.validate()
        # form.validate() 用于验证表单的每个字段（控件），都满足时返回值为True
        if form.validate_on_submit():
            username = form.user_name.data
            password = form.password.data
            password2 = form.password2.data
            return 'login success'
        else:
            # flask的form使用一个字典来储存各控件的errors列表
            # print(type(form.errors))
            # 输出密码字段导致validate_on_submit为false的错误原因（两种方式）
            print(form.errors['password'])
            print(form.password.errors)
            return render_template('register.html',form=form)

if __name__ == '__main__':
    app.run()
```
