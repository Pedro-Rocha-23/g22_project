"""
apps_subform.py  —  Header + lines CRUD (1-to-many).

Called by app.py route  /subform/<cname>
cname format:  "HeaderClass_LineClass"   e.g. "University_Uni_grant"

The header class is navigated record by record.
The lines class shows all records linked to the current header.
"""
from flask import render_template, request, session

from classes.university import University
from classes.uni_grant  import Uni_grant
from classes.grant      import Grant

# ── Map string names → class objects ──────────────────────────────────────────
CLASS_MAP = {
    'University': University,
    'Uni_grant':  Uni_grant,
    'Grant':      Grant,
}

_prev_option = {}

def apps_subform(cname):
    global _prev_option

    # Parse "University_Uni_grant"
    parts = cname.split('_', 1)
    if len(parts) != 2:
        return f"<h2>Formato inválido: '{cname}'. Use 'Header_Line'.</h2>", 400

    hname, lname = parts[0], parts[1]
    hcls = CLASS_MAP.get(hname)
    lcls = CLASS_MAP.get(lname)
    if not hcls or not lcls:
        return f"<h2>Classe não encontrada: '{hname}' ou '{lname}'.</h2>", 404

    # Foreign key linking lines to header: second attribute of line class
    fk_attr = lcls.att[1][1:]   # e.g. '_university_id' → 'university_id'

    prev    = _prev_option.get(cname, '')
    option  = request.args.get('option', '')
    butshow, butedit = 'enabled', 'disabled'

    # ── Header navigation ──────────────────────────────────────────────────────
    if option == 'first':    hcls.first()
    elif option == 'previous': hcls.previous()
    elif option == 'next':     hcls.nextrec()
    elif option == 'last':     hcls.last()

    # ── Line CRUD ──────────────────────────────────────────────────────────────
    elif option == 'edit':
        butshow, butedit = 'disabled', 'enabled'

    elif option == 'delete_line':
        line_id = int(request.args.get('line_id', 0))
        if line_id in lcls.obj:
            lcls.remove(line_id)

    elif option == 'insert_line':
        butshow, butedit = 'disabled', 'enabled'

    elif option == 'cancel':
        pass

    elif prev == 'insert_line' and option == 'save':
        hobj   = hcls.current()
        new_id = lcls.get_id(0)
        parts2 = [str(new_id), str(hobj.id)]
        for att in lcls.att[2:]:            # skip _id and fk
            parts2.append(request.form.get(att[1:], ''))
        obj = lcls.from_string(';'.join(parts2))
        lcls.insert(obj.id)

    elif prev == 'edit' and option == 'save':
        line_id = int(request.form.get('line_id', 0))
        obj = lcls.obj.get(line_id)
        if obj:
            for att in lcls.att[2:]:        # skip _id and fk
                field = att[1:]
                val   = request.form.get(field, '')
                current = getattr(obj, field)
                try:
                    if isinstance(current, int):   val = int(val)
                    elif isinstance(current, float): val = float(val)
                except (ValueError, TypeError):    pass
                setattr(obj, field, val)
            lcls.update(obj.id)

    _prev_option[cname] = option

    # ── Build context ──────────────────────────────────────────────────────────
    hobj  = hcls.current()
    hflds = {att[1:]: getattr(hobj, att) for att in hcls.att} if hobj else {}

    # Lines belonging to current header
    if hobj:
        lines = [lcls.obj[k] for k in lcls.lst
                 if getattr(lcls.obj[k], fk_attr) == hobj.id]
    else:
        lines = []

    # For Uni_grant lines: resolve grant title for display
    grant_map = {g.id: g.title for g in Grant.obj.values()}

    return render_template(
        'subform.html',
        hname    = hname,
        lname    = lname,
        hheader  = hcls.header,
        lheader  = lcls.header,
        hatt     = hcls.att,
        latt     = lcls.att,
        hdes     = hcls.des,
        ldes     = lcls.des,
        hflds    = hflds,
        lines    = lines,
        butshow  = butshow,
        butedit  = butedit,
        total    = len(hcls.lst),
        ulogin   = session.get('user'),
        grant_map= grant_map,
        grants   = [(g.id, g.title) for g in Grant.obj.values()],
    )
