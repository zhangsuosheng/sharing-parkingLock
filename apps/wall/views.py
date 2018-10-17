from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from wall.utils import sanitize

from wall.models import Wall, WallItem, WallComment
from wall.forms import WallItemForm, WallItemCommentForm

from django.utils import simplejson
import logging, traceback, pprint

@login_required
def home( request, slug, template_name='wall/home.html'):
    """
    A view that shows all of the wall items.
    (Use template_name of 'wall/recent.html' to see just recent items.)
    """
    wall = get_object_or_404( Wall, slug=slug )

    return render_to_response( template_name,
        {   "wall": wall,
            "form": WallItemForm(),
            "items" : wall.active_items_set(),
            'commentform':WallItemCommentForm()
        },
        context_instance = RequestContext( request ))

@login_required
def add(request, slug, form_class=WallItemForm,
            template_name='wall/home.html',
            success_url=None, can_add_check=None):
    """
    A view for adding a new WallItem.

    The optional 'can_add_check' callback passes you a user and a wall.
      Return True if the user is authorized and False otherwise.
      (Default: any user can create a wall item for the given wall.)
    """
    wall = get_object_or_404( Wall, slug=slug )
    if success_url == None:
        success_url = reverse( 'wall_home', args=(slug,))
    if request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            posting = form.cleaned_data['posting']
            
            
            if (wall.max_item_length) and (len(posting) > wall.max_item_length):
                body = posting[:wall.max_item_length]
            else:
                body = posting
                
            body = sanitize(body)
            item = WallItem( author=request.user, wall=wall, body=body, created_at=datetime.now() )
            item.save()
            
            if request.FILES:
                file_content = request.FILES['img']
                item.item_pic.save(file_content.name, file_content, save=True)
            
            return HttpResponseRedirect(success_url)
        else:
            print 'errors'
            print form.errors
    else:
        form = form_class( help_text="Input text for a new item.<br/>(HTML tags will %sbe ignored. The item will be trimmed to %d characters.)" % ("not " if wall.allow_html else "", wall.max_item_length))
    return render_to_response(template_name,
        { 'form': form, 'wall': wall },
        context_instance = RequestContext( request ))

@login_required
def delete(request, id):

    item = get_object_or_404( WallItem, id=int(id) )
    success_url = reverse( 'wall_home', args=(item.wall.slug,))
    
    response_dict = {}
    response_dict.update({'itemid':id})
    
    if not item.deleteable_by(request.user):
        response_dict.update({'success': False})
    
    else:
        try:
            item.deleted = True
            item.save()
            response_dict.update({'success': True})
        except:
            response_dict.update({'success': False})

    if request.is_ajax():
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    
    return HttpResponseRedirect(success_url)
    
@login_required
def commentadd( request, wallitemid, form_class=WallItemCommentForm,
            template_name='wall/comment.html',
            success_url='wall_home'):
    """
    A view for adding a new WallItemComment.

    """
    
    if not request.POST:
        form = form_class( help_text="Input text for a new comment.<br/>(HTML tags will be ignored.)")
        return render_to_response(template_name, { 'commentform': form, 'wallitemid': wallitemid }, context_instance = RequestContext( request ))

    else:
        form = form_class(request.POST)
        wallitem = get_object_or_404( WallItem, id=wallitemid )
        response_dict = {}
        response_dict.update({'itemid':wallitem.id})
            
        if form.is_valid():
            
            commentbody = form.cleaned_data['comment']
            
            max_length = WallComment._meta.get_field('body').max_length
            
            if (len(commentbody) > max_length):
                commentbody = commentbody[:max_length]
            else:
                commentbody = commentbody
                
            commentbody = sanitize(commentbody)
            
            comment = WallComment( author=request.user, wallitem=wallitem, body=commentbody, created_at=datetime.now() )
            comment.save()
            
            response_dict.update({'itemid':comment.wallitem.id,'comment': comment.body, 'commentid':comment.id, 'author': comment.author.get_profile().name,'created_at':comment.created_at.strftime('%b. %d, %Y %I:%M %p') })  #Feb. 14, 2012, 2:02 p.m
            response_dict.update({'success': True})
        else:
            print form.errors
            response_dict.update({'errors': form.errors})
            
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
        
        return render_to_response(template_name, { 'commentform': form, 'wallitemid': wallitemid }, context_instance = RequestContext( request ))
    
@login_required
def commentdelete(request, id):

    comment = get_object_or_404( WallComment, id=int(id) )
    success_url = reverse( 'wall_home', args=(comment.wallitem.wall.slug,))

    response_dict = {}
    response_dict.update({'commentid':id})
    
    if not comment.deleteable_by(request.user):
        response_dict.update({'success': False})
        
    else:
        try:
            comment.deleted = True
            comment.save()
            response_dict.update({'success': True})
    
        except:
            response_dict.update({'success': False})

    if request.is_ajax():
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    
    return HttpResponseRedirect(success_url)

def wall_image(request,wallitemid):
    wallitem = get_object_or_404( WallItem, id=wallitemid )
    
    return render_to_response('wall/wall_image.html', {
        'item': wallitem
    }, context_instance=RequestContext(request))
