import uuid

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from inject.forms import InjectForm

import worker

import cass

import logging
logger = logging.getLogger(__name__)

NUM_PER_PAGE = 40

def inject_data(request):
    logger.info("NEW Function inject_data")
    context = {}
    if request.is_ajax():
        # ajax
        logger.info("AJAX REQUEST")
    else:
        # regular
        logger.info("NON-AJAX REQUEST")

    if request.method == 'POST':
        inject_form = InjectForm(request.POST)
        next = request.REQUEST.get('next')
        context = {
            'inject_form': inject_form,
            'next': next,
        }
        if inject_form.is_valid():
            #
            # do work here
            #
            logger.info("WORK! form_data: %s  ", inject_form.cleaned_data )
            tmpusers = inject_form.cleaned_data['numusers']
            tmptweet = inject_form.cleaned_data['numtweets']
            tmpdelay = inject_form.cleaned_data['secdelay']
            tmpflag = inject_form.cleaned_data['distroflag']

            inject_job = worker.Worker()
            inject_job.inject(tmpusers, tmptweet, tmpdelay, tmpflag)
        else:
            temp_errors = inject_form.errors()
            context = {
                    'inject_form' : temp_errors
                    }
                    
            return render(request, 'inject/control.html', context)


    else:
        inject_form = InjectForm(initial={'numusers':10,'numtweets':10,'secdelay':0,'distroflag':False} )
        next = request.REQUEST.get('next')
        context = {
            'inject_form': inject_form,
            'next': next,
        }
    #

    #return render_to_response('inject/control.html', context, context_instance=RequestContext(request))
    return render(request, 'inject/control.html', context )

