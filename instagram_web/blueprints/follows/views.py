from flask import Blueprint, url_for, redirect, flash
from models.user import User
from models.followerfollowing import FollowerFollowing
from flask_login import current_user, login_required

follows_blueprint = Blueprint('follows', __name__, template_folder='templates')


@follows_blueprint.route('/<idol_id>', methods=['POST'])
@login_required
def create(idol_id):
  # use get_or_none in case there is no user id
    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash('No user found with this id!')
        return redirect(url_for('home'))

    new_follow = FollowerFollowing(
        fan_id=current_user.id,
        idol_id=idol.id
    )

    # check if user is private or not. If user.private is False, then Follower.Following = True

    if not idol.is_private:
        new_follow.approved = True

    # assuming EVERYONE you are trying to follow is private
    if not new_follow.save():
        flash('Unable to follow this user!')
        return redirect(url_for('users.show', username=idol.username))

    # using hybrid property to change FollowerFollowing.approved to True
    if new_follow.is_approved:
        flash(f'You are now following {idol.username}')
        return redirect(url_for('users.show', username=idol.username))

    flash('Follow request sent! Please wait for approval!')
    return redirect(url_for('users.show', username=idol.username))


@follows_blueprint.route('/<idol_id>/unfollow', methods=['POST'])
def delete(idol_id):
    follow = FollowerFollowing.get_or_none((FollowerFollowing.idol_id == idol_id) and (
        FollowerFollowing.fan_id == current_user.id))

    if follow.delete_instance():
        flash(f'You have unfollowed {follow.idol.username}')
        return redirect(url_for('users.show', username=follow.idol.username))
