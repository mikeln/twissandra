import uuid

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from inject.forms import InjectForm

import cass

import logging
logger = logging.getLogger(__name__)

NUM_PER_PAGE = 40

def inject_data(request):
    logger.debug("NEW Function inject_data")

    #start = request.GET.get('start')
    #tweets, next_timeuuid = cass.get_userline(
    #    cass.PUBLIC_USERLINE_KEY, start=start, limit=NUM_PER_PAGE)
    #context = {
    #    'tweets': tweets,
    #    'next': next_timeuuid,
    #}
    return render_to_response(
        'inject/control.html', context, context_instance=RequestContext(request))


def userline(request, username=None):
    try:
        user = cass.get_user_by_username(username)
    except cass.DatabaseError:
        raise Http404

    # Query for the friend ids
    friend_usernames = []
    if request.user['is_authenticated']:
        friend_usernames = cass.get_friend_usernames(username) + [username]

    # Add a property on the user to indicate whether the currently logged-in
    # user is friends with the user
    is_friend = username in friend_usernames

    start = request.GET.get('start')
    tweets, next_timeuuid = cass.get_userline(username, start=start, limit=NUM_PER_PAGE)
    context = {
        'user': user,
        'username': username,
        'tweets': tweets,
        'next': next_timeuuid,
        'is_friend': is_friend,
        'friend_usernames': friend_usernames,
    }
    return render_to_response(
        'tweets/userline.html', context, context_instance=RequestContext(request))
