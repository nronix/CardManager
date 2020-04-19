from flask import Blueprint, render_template,request
from . import db
from flask_login import login_required, current_user
from .models import Cards
import json
from sqlalchemy.sql import func
from .utils import getcards_trim_data

main = Blueprint('main',__name__)

@main.route('/')

def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def profile():
    query = Cards.query
    yearby_unused = dict()
    yearby_used = dict()
    summary = dict()
    years = ['2020','2021','2022','2023','2024','2025','2026']
    summary['used_cards'] = query.filter_by(used=True).count()
    summary['expired'] = query.filter_by(expired=True).count()
    summary['remaining'] = query.filter_by(used=None).count()
    total_amount = query.with_entities(func.sum(Cards.amount).label('total')).first()
    progress = query.filter_by(in_progress=True).count()
    # count all un used cards by year
    for year in years:
        yearby_unused[year] = query.filter_by(used=None,year=year).count()
    # count all used cards by year
    for year in years:
        yearby_used[year] = query.filter_by(used=True,year=year).count()
    print(summary)
    print(yearby_unused)
    print(yearby_used)
    print(total_amount)
    total_cards = summary['used_cards']+summary['remaining']+summary['expired']
    user_percent = round((summary['used_cards']+summary['expired'])/total_cards * 100)
    return render_template('profile.html',name=current_user.name,remaining=summary['remaining'],total_amount=total_amount.total
                           ,total_used=summary['used_cards'],usage_per=user_percent,progress=progress
                           ,summary=json.dumps(summary),
                           yearby_unused=json.dumps(yearby_unused),
                           yearby_used=json.dumps(yearby_used))

@main.route('/dashboard/<querytype>')
@login_required
def profile_querytype(querytype):
    query = Cards.query
    if querytype == 'all':
        cards = query.all()
    elif querytype == 'available':
        cards = query.filter_by(used=None,in_progress=False)
    elif querytype == 'progress':
        cards = query.filter_by(in_progress=True)
    elif querytype == 'expired':
        cards = query.filter_by(expired=True)
    elif querytype  == 'used':
        cards = query.filter_by(used=True)
    else:
        cards = []
    result = getcards_trim_data(cards)
    return render_template('profile-data.html',len=len(result),cards=result)

@main.route('/dashboard/update/<id>')
@login_required
def update_id(id):
    #print("marking in progress id "+id)
    action = request.args.get('action')
    if action is not None:
        print(action)
        updated=dict()
        updated['used_on_google'] = request.args.get('used_on_google')
        updated['used_on_amazon'] = request.args.get('used_on_amazon')
        updated['amount'] = request.args.get('amount')
        updated['usage'] = request.args.get('usage')
        if updated['amount'] is None or updated['amount'] is "":
            updated['amount'] = 0
        if updated['used_on_google'] is None or updated['used_on_google'] is "":
            updated['used_on_google'] = False
        else:
            if updated['used_on_google'] == 'true':
                updated['used_on_google'] = True
            else:
                updated['used_on_google'] = False
        if updated['used_on_amazon'] is None or updated['used_on_amazon'] is "":
            updated['used_on_amazon'] = False
        else:
            if updated['used_on_amazon'] == 'true':
                updated['used_on_amazon'] = True
            else:
                updated['used_on_amazon'] = False
        if updated['usage'] is None or updated['usage'] is "":
            updated['usage'] = "unset"
        updated['used'] = True
        updated['waste'] = False
        updated['expired'] = False
        updated['in_progress']= False
        print(updated)
        Cards.query.filter(Cards.id == id).update(updated)
    else:
        Cards.query.filter(Cards.id == id).update({"in_progress":True})
    db.session.commit()
    return id

@main.route('/dashboard/delete/<id>')
@login_required
def trash_id(id):
    Cards.query.filter(Cards.id == id).update({"waste":True,"amount":0,"used_on_google":False,
                                               "used_on_amazon":False,"expired":True,
                                               "used":False,"usage":"waste","in_progress":False})
    db.session.commit()
    return id