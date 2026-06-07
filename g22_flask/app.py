import os
from flask import Flask, render_template, request, session, redirect, url_for

from classes.university import University
from classes.lab import Lab
from classes.grant import Grant
from classes.director import Director
from classes.uni_grant import Uni_grant
from classes.userlogin import Userlogin
from classes.region import Region
from subs.apps_plotly import grafico_circular, grafico_idades_diretores, grafico_linhas

app = Flask(__name__)
app.secret_key = "g22_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "g22_db.db")


prev_options = {
    "university": "",
    "lab": "",
    "grant": "",
    "director": "",
    "uni_grant": "",
    "userlogin": ""
}


def obj_id_value(item):
    return getattr(item, "id", item)


def sort_by_id(cls):
    cls.lst.sort(key=lambda x: int(obj_id_value(x)))
    cls.pos = 0


def iter_objects(cls):
    for item in cls.lst:
        if hasattr(item, "id"):
            yield item
        else:
            yield cls.obj[item]


def current_obj(cls):
    if len(cls.lst) == 0:
        return None

    try:
        return cls.current()
    except Exception:
        item = cls.lst[cls.pos]
        if hasattr(item, "id"):
            return item
        return cls.obj[item]


def get_field(obj, possible_names):
    for name in possible_names:
        if hasattr(obj, name):
            return getattr(obj, name)

        private_name = "_" + name
        if hasattr(obj, private_name):
            return getattr(obj, private_name)

    return ""


def set_field(obj, possible_names, value):
    for name in possible_names:
        if hasattr(obj.__class__, name):
            try:
                setattr(obj, name, value)
                return
            except AttributeError:
                pass

        if hasattr(obj, name):
            try:
                setattr(obj, name, value)
                return
            except AttributeError:
                pass

        private_name = "_" + name
        if hasattr(obj, private_name):
            setattr(obj, private_name, value)
            return


    setattr(obj, possible_names[0], value)



University.read(DB_PATH)
Lab.read(DB_PATH)
Grant.read(DB_PATH)
Director.read(DB_PATH)
Uni_grant.read(DB_PATH)
Region.read(DB_PATH)
Userlogin.read(DB_PATH)

sort_by_id(University)
sort_by_id(Lab)
sort_by_id(Grant)
sort_by_id(Director)
sort_by_id(Uni_grant)
sort_by_id(Region)
sort_by_id(Userlogin)



def get_user_name(obj):
    return get_field(obj, ["user", "username"])


def set_user_name(obj, value):
    set_field(obj, ["user", "username"], value)


def get_user_group(obj):
    return get_field(obj, ["usergroup", "group"])


def set_user_group(obj, value):
    set_field(obj, ["usergroup", "group"], value)


def get_user_password(obj):
    return get_field(obj, ["password"])


def logged_user_obj():
    username = session.get("user")

    if username is None:
        return None

    for obj in iter_objects(Userlogin):
        if str(get_user_name(obj)) == str(username):
            return obj

    return None


def logged_user_group():
    obj = logged_user_obj()

    if obj is None:
        return ""

    return get_user_group(obj)


def check_password(user, password):
    for obj in iter_objects(Userlogin):
        if str(get_user_name(obj)) == str(user):
            if str(get_user_password(obj)) == str(password):
                Userlogin.user_id = obj.id
                Userlogin.username = get_user_name(obj)
                return "Valid"
            return "Invalid password"

    return "Invalid user"



@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user") is None:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        ulogin=session.get("user")
    )



@app.route("/login")
def login():
    if session.get("user") is not None:
        return redirect(url_for("index"))

    return render_template(
        "login.html",
        id=0,
        user="",
        password="",
        ulogin=session.get("user"),
        resul=""
    )


@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/chklogin", methods=["POST", "GET"])
def chklogin():
    user = request.form.get("user", "")
    password = request.form.get("password", "")

    resul = check_password(user, password)

    if resul == "Valid":
        session["user"] = user
        return redirect(url_for("index"))

    return render_template(
        "login.html",
        id=0,
        user=user,
        password="",
        ulogin=session.get("user"),
        resul=resul
    )



def class_page(cls, template_name, page_key, fields):
    if session.get("user") is None:
        return redirect(url_for("login"))

    butshow, butedit = "enabled", "disabled"
    msg = ""
    option = request.args.get("option")
    prev_option = prev_options[page_key]

    if option == "edit":
        butshow, butedit = "disabled", "enabled"

    elif option == "delete":
        if len(cls.lst) > 0:
            obj = current_obj(cls)
            cls.remove(obj.id)
            sort_by_id(cls)

            if len(cls.lst) > 0 and cls.pos >= len(cls.lst):
                cls.pos = len(cls.lst) - 1

    elif option == "insert":
        butshow, butedit = "disabled", "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        values = [request.form.get(form_name, "") for form_name, _attr_names in fields]
        strobj = str(cls.get_id(0)) + ";" + ";".join(values)

        obj = cls.from_string(strobj)
        cls.insert(obj.id)
        sort_by_id(cls)
        cls.last()

    elif prev_option == "edit" and option == "save":
        obj = current_obj(cls)

        if obj is not None:
            for form_name, attr_names in fields:
                set_field(obj, attr_names, request.form.get(form_name, ""))

            cls.update(obj.id)
            sort_by_id(cls)

    elif option == "first":
        cls.first()

    elif option == "previous":
        cls.previous()

    elif option == "next":
        cls.nextrec()

    elif option == "last":
        cls.last()

    elif option == "exit":
        return redirect(url_for("index"))

    prev_options[page_key] = option

    context = {
        "butshow": butshow,
        "butedit": butedit,
        "msg": msg,
        "ulogin": session.get("user")
    }

    if option == "insert" or len(cls.lst) == 0:
        context["id"] = cls.get_id(0)
        for form_name, _attr_names in fields:
            context[form_name] = ""
    else:
        obj = current_obj(cls)
        context["id"] = obj.id
        for form_name, attr_names in fields:
            context[form_name] = get_field(obj, attr_names)

    return render_template(template_name, **context)


@app.route("/university", methods=["GET", "POST"])
def university():
    return class_page(
        University,
        "university.html",
        "university",
        [
            ("name", ["name"]),
            ("creation_date", ["creation_date"]),
            ("region_id", ["region_id"])
        ]
    )


@app.route("/lab", methods=["GET", "POST"])
def lab():
    return class_page(
        Lab,
        "lab.html",
        "lab",
        [
            ("extra_info", ["extra_info"]),
            ("university_id", ["university_id"])
        ]
    )


@app.route("/grant", methods=["GET", "POST"])
def grant():
    return class_page(
        Grant,
        "grant.html",
        "grant",
        [
            ("title", ["title"]),
            ("category", ["category"]),
            ("director_id", ["director_id"])
        ]
    )


@app.route("/director", methods=["GET", "POST"])
def director():
    return class_page(
        Director,
        "director.html",
        "director",
        [
            ("director_name", ["director_name", "name"]),
            ("dob", ["dob", "date_of_birth"])
        ]
    )


@app.route("/uni_grant", methods=["GET", "POST"])
def uni_grant():
    return class_page(
        Uni_grant,
        "uni_grant.html",
        "uni_grant",
        [
            ("university_id", ["university_id"]),
            ("grant_id", ["grant_id"]),
            ("amount", ["amount"]),
            ("start_date", ["start_date"])
        ]
    )



@app.route("/Userlogin", methods=["GET", "POST"])
def userlogin():
    if session.get("user") is None:
        return redirect(url_for("login"))

    butshow, butedit = "enabled", "disabled"
    msg = ""
    option = request.args.get("option")
    group = logged_user_group()
    prev_option = prev_options["userlogin"]

    if option == "edit":
        butshow, butedit = "disabled", "enabled"

    elif option == "delete":
        if group == "admin":
            if len(Userlogin.lst) > 0:
                obj = current_obj(Userlogin)
                Userlogin.remove(obj.id)
                sort_by_id(Userlogin)

                if len(Userlogin.lst) > 0 and Userlogin.pos >= len(Userlogin.lst):
                    Userlogin.pos = len(Userlogin.lst) - 1
        else:
            msg = "Only admins can delete users"

    elif option == "insert":
        if group == "admin":
            butshow, butedit = "disabled", "enabled"
        else:
            msg = "Only admins can insert users"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        if group == "admin":
            strobj = (
                str(Userlogin.get_id(0)) + ";"
                + request.form.get("user", "") + ";"
                + request.form.get("usergroup", "") + ";"
                + request.form.get("password", "")
            )

            obj = Userlogin.from_string(strobj)
            Userlogin.insert(obj.id)
            sort_by_id(Userlogin)
            Userlogin.last()
        else:
            msg = "Only admins can insert users"

    elif prev_option == "edit" and option == "save":
        if group == "admin":
            obj = current_obj(Userlogin)

            if obj is not None:
                set_user_name(obj, request.form.get("user", ""))
                set_user_group(obj, request.form.get("usergroup", ""))

                password = request.form.get("password", "")
                if password != "":
                    set_field(obj, ["password"], password)

                Userlogin.update(obj.id)
                sort_by_id(Userlogin)

        else:
            obj = logged_user_obj()

            if obj is not None:
                password = request.form.get("password", "")

                if password != "":
                    set_field(obj, ["password"], password)
                    Userlogin.update(obj.id)
                else:
                    msg = "Password not changed"

    elif option == "first":
        if group == "admin":
            Userlogin.first()

    elif option == "previous":
        if group == "admin":
            Userlogin.previous()

    elif option == "next":
        if group == "admin":
            Userlogin.nextrec()

    elif option == "last":
        if group == "admin":
            Userlogin.last()

    elif option == "exit":
        return redirect(url_for("index"))

    prev_options["userlogin"] = option

    if group == "admin":
        if option == "insert" or len(Userlogin.lst) == 0:
            id = Userlogin.get_id(0)
            user = ""
            usergroup = ""
        else:
            obj = current_obj(Userlogin)
            id = obj.id
            user = get_user_name(obj)
            usergroup = get_user_group(obj)
    else:
        obj = logged_user_obj()

        if obj is None:
            id = 0
            user = ""
            usergroup = ""
            msg = "User not found"
        else:
            id = obj.id
            user = get_user_name(obj)
            usergroup = get_user_group(obj)

    return render_template(
        "userlogin.html",
        butshow=butshow,
        butedit=butedit,
        id=id,
        user=user,
        usergroup=usergroup,
        group=group,
        msg=msg,
        ulogin=session.get("user")
    )



@app.route("/analise")
def analise():
    return render_template("analise.html", ulogin=session.get("user"))


@app.route("/analise/circular")
def analise_circular(): return grafico_circular()

@app.route("/analise/idades")
def analise_idades(): return grafico_idades_diretores()

@app.route("/analise/linhas")
def analise_linhas(): return grafico_linhas()


if __name__ == "__main__":
    app.run()
