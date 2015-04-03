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
    logger.info("NEW Function inject_data")

    context = {}
    if request.method == 'POST':
        inject_form = InjectForm(request.POST)
        next = request.REQUEST.get('next')
        context = {
            'inject_form': inject_form,
            'next': next,
        }
        if form.is_valid():
            #
            # do work here
            #
            logger.info("TODO: work")
    else:
        inject_form = InjectForm(initial={'numusers':10,'numtweets':10,'secdelay':0,'distroflag':False} )
        next = request.REQUEST.get('next')
        context = {
            'inject_form': inject_form,
            'next': next,
        }
    #

    return render_to_response(
        'inject/control.html', context, context_instance=RequestContext(request))

