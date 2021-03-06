import uuid

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse

from inject.forms import InjectForm

import worker

import cass

import logging
logger = logging.getLogger(__name__)

import json

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
            #tmpflag = inject_form.cleaned_data['distroflag']
            tmpflag = 0

            inject_job = worker.Worker()
            tmpu, tmpw, tmpt = inject_job.inject(tmpusers, tmptweet, tmpdelay, tmpflag)
            
            response_data={}
            response_data['newusers'] = tmpu
            response_data['newtweets'] = tmpw
            response_data['newtotal'] = tmpt
            return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                    )
            #return render(request, 'inject/control.html', context)
        else:
            context = {}
            return render(request, 'inject/control.html', context)


    else:
        inject_form = InjectForm(initial={'numusers':10,'numtweets':10,'secdelay':0} )
        next = request.REQUEST.get('next')
        context = {
            'inject_form': inject_form,
            'next': next,
        }
    #
    #return render_to_response('inject/control.html', context, context_instance=RequestContext(request))
    return render(request, 'inject/control.html', context )

