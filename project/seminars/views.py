# project/items/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from project import db
from project.models import Items, User
from .forms import ItemsForm, EditItemsForm


# CONFIG
seminars_blueprint = Blueprint('seminars', __name__, template_folder='templates')


# ROUTES
@seminars_blueprint.route('/all_seminars', methods=['GET', 'POST'])
@login_required
def all_seminars():
    """Render homepage"""
    all_seminars = Seminars.query.fetchall()
    return render_template('all_seminar.html', items=all_user_seminars)


@seminars_blueprint.route('/<seminars_id>')
@login_required
def watch_seminar():
    return render_template('watch_seminar.html')


@seminars_blueprint.route('/<seminars_id>/question')
@login_required
def question_seminar():
    return render_template('question_seminar.html', form=form)


@seminars_blueprint.route('/add_seminar', methods=['GET', 'POST'])
@login_required
def add_seminar():
    form = ItemsForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_item = Items(form.name.data, form.notes.data,
                                 current_user.id)
                db.session.add(new_item)
                db.session.commit()
                message = Markup(
                    "<strong>Well done!</strong> Item added successfully!")
                flash(message, 'success')
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                message = Markup(
                    "<strong>Oh snap!</strong>! Unable to add item.")
                flash(message, 'danger')
    return render_template('add_item.html', form=form)


@seminars_blueprint.route('/edit_seminar/<seminars_id>', methods=['GET', 'POST'])
@login_required
def edit_seminar(seminars_id):
    form = EditItemsForm(request.form)
    item_with_user = db.session.query(Items, User).join(User).filter(Items.id == seminars_id).first()
    if item_with_user is not None:
        if current_user.is_authenticated and item_with_user.Items.user_id == current_user.id:
            if request.method == 'POST':
                if form.validate_on_submit():
                    try:
                        item = Items.query.get(seminars_id)
                        item.name = form.name.data
                        item.notes = form.notes.data
                        db.session.commit()
                        message = Markup("Item edited successfully!")
                        flash(message, 'success')
                        return redirect(url_for('home'))
                    except:
                        db.session.rollback()
                        message = Markup(
                            "<strong>Error!</strong> Unable to edit item.")
                        flash(message, 'danger')
            return render_template('edit_item.html', item=item_with_user, form=form)
        else:
            message = Markup(
                "<strong>Error!</strong> Incorrect permissions to access this item.")
            flash(message, 'danger')
    else:
        message = Markup("<strong>Error!</strong> Item does not exist.")
        flash(message, 'danger')
    return redirect(url_for('home'))


@seminars_blueprint.route('/delete_seminar/<seminars_id>', methods=['GET', 'POST'])
@login_required
def delete_seminar(seminars_id):
    item_with_user = db.session.query(Items, User).join(User).filter(Items.id == seminars_id).first()
    if item_with_user is not None:
        items = Items.query.filter_by(id=seminars_id)
        if current_user.is_authenticated and item_with_user.Items.user_id == current_user.id:
            print(request.method)
            if request.method == 'POST':
                try:
                    db.session.delete(items[0])
                    db.session.commit()
                    message = Markup("<strong>Done.</strong> You have deleted item " + str(seminars_id) + ".")
                    flash(message, 'success')
                    return redirect(url_for('home'))
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    message = Markup(
                        "<strong>Error!</strong> Unable to delete item.")
                    flash(message, 'danger')
            return render_template('delete_item.html', items=items)
        else:
            message = Markup(
                "<strong>Error!</strong> Incorrect permissions to access this item.")
            flash(message, 'danger')
    else:
        message = Markup("<strong>Error!</strong> Item does not exist.")
        flash(message, 'danger')
    return redirect(url_for('home'))
