from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from models.image import Image
from models.user import User
from models.donation import Donation
from instagram_web.util.braintree import generate_client_token
from instagram_web.util.braintree import complete_transaction
from instagram_web.util.sendgrid import send_email

donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)
    client_token = generate_client_token()
    if not image:
        flash('Unable to find image with the provided id.')
        return redirect(url_for('home'))
    else:
        return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>/checkout', methods=['POST'])
def create(image_id):
    payment_nonce = request.form.get('payment_nonce')
    amount = request.form.get('donation_amount')
    image = Image.get_or_none(Image.id == image_id)
    # email = Image.get_or_none(Image.user.email == email)

    if not image:
        flash('Unable to find image. Please try again.')
        return redirect(url_for('home'))

    if not amount or round(int(amount), 2) == 0:
        flash('Please insert a proper amount')
        return redirect(url_for('donations.new', image_id=image.id))

    if not payment_nonce:
        flash('Error with payment system. Please try again.')
        return redirect(url_for('users.show', username=image.user.username))

    if not complete_transaction(payment_nonce, amount):
        flash('Something went wrong')
        return redirect(url_for('donations.new', image_id=image.id))

    #SEND EMAIL#
    send_email()

    #SAVING DONATIONS TO THE DATABASE#
    new_donation = Donation(
        user_id=current_user.id,
        amount=amount,
        image_id=image.id
    )

    if not new_donation.save():
        flash('Unable to complete the transaction!')
        return redirect(url_for('donations.new', image_id=image.id))

    flash('Donation successful!')
    return redirect(url_for('users.show', username=image.user.username))
