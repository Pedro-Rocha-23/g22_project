"""
apps_gform.py  —  Generic CRUD handler for any Gclass subclass.

Called by app.py route  /gform/<cname>
The class name (cname) is used to look up the right class object
from the ENTITIES dict, so no code changes are needed when a new class is added.
"""
from flask import render_template, request, session
import importlib, sys

# ── Map class name → class object ─────────────────────────────────────────────
# Add new entities here without touching app.py or gform.html
from classes.university import University
from classes.lab        import Lab
from classes.grant      import Grant
from classes.director   import Director

ENTITIES = {
    'University': University,
    'Lab':        Lab,
    'Grant':      Grant,
    'Director':   Director,
}

# ── Extra related data sent to the template (for dropdown selects) ─────────────
def _extras(cname):
    """Return a dict of extra context variables needed by a specific class form."""
    from classes.university import University
    from classes.director   import Director
    extras = {}
    if cname == 'Lab':
        extras['universities'] = [(u.id, u.name) for u in University.obj.values()]
    if cname == 'Grant':
        extras['directors'] = [(d.id, d.director_name) for d in Director.obj.values()]
    return extras

# ── State: one prev_option per class, stored by name ──────────────────────────
_prev_option = {}

def apps_gform(cname):
    global _prev_option

    cls = ENTITIES.get(cname)
    if cls is None:
        return f"<h2>Classe '{cname}' não encontrada.</h2>", 404

    prev = _prev_option.get(cname, '')
    butshow, butedit = 'enabled', 'disabled'
    option = request.args.get('option', '')

    # ── CRUD option handling ───────────────────────────────────────────────────
    if option == 'edit':
        butshow, butedit = 'disabled', 'enabled'

    elif option == 'delete':
        obj = cls.current()
        if obj:
            cls.remove(obj.id)
            if not cls.previous():
                cls.first()

    elif option == 'insert':
        butshow, butedit = 'disabled', 'enabled'

    elif option == 'cancel':
        pass

    elif prev == 'insert' and option == 'save':
        new_id = cls.get_id(0)
        # Build the string from form fields in the order defined by cls.att
        parts = [str(new_id)]
        for att in cls.att[1:]:          # skip _id, already set
            parts.append(request.form.get(att[1:], ''))   # strip leading '_'
        obj = cls.from_string(';'.join(parts))
        cls.insert(obj.id)
        cls.last()

    elif prev == 'edit' and option == 'save':
        obj = cls.current()
        if obj:
            for att in cls.att[1:]:
                field = att[1:]          # strip leading '_'
                val   = request.form.get(field, '')
                # Cast to the right type based on the current attribute value
                current = getattr(obj, field)
                try:
                    if isinstance(current, int):
                        val = int(val)
                    elif isinstance(current, float):
                        val = float(val)
                except (ValueError, TypeError):
                    pass
                setattr(obj, field, val)
            cls.update(obj.id)

    elif option == 'first':    cls.first()
    elif option == 'previous': cls.previous()
    elif option == 'next':     cls.nextrec()
    elif option == 'last':     cls.last()

    _prev_option[cname] = option

    # ── Build context dict from current object ─────────────────────────────────
    obj = cls.current()

    if option == 'insert' or len(cls.lst) == 0:
        # Blank form for new record
        fields = {att[1:]: '' for att in cls.att}
        fields[cls.att[0][1:]] = cls.get_id(0)   # auto-increment id
    else:
        fields = {att[1:]: getattr(obj, att) for att in cls.att}
        # Also expose computed properties if they exist (e.g. age)
        for prop in ('age',):
            if hasattr(obj, prop):
                fields[prop] = getattr(obj, prop)

    return render_template(
        'gform.html',
        cname    = cname,
        header   = cls.header,
        att      = cls.att,           # ['_id', '_name', ...]
        des      = cls.des,           # ['Id', 'Name', ...]
        fields   = fields,            # {'id': 1, 'name': 'MIT', ...}
        butshow  = butshow,
        butedit  = butedit,
        total    = len(cls.lst),
        ulogin   = session.get('user'),
        **_extras(cname),             # universities=[], directors=[], etc.
    )
