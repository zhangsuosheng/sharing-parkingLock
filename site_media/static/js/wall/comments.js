
$(document).ready(function() {
	$("div.comment-form").hide();
});


$("div.wallitem").delegate("span.comment-toggle", "click", function() {
	wallitemdiv = $(this).parents("div.wallitem");
	$("div.comment-form",wallitemdiv).toggle();
    $("textarea",wallitemdiv).focus();
    return false;
});

$("div.comment-form").delegate("textarea", "click", function() {
	wallitemdiv = $(this).parents("div.wallitem");
	$("div.comment-error",wallitemdiv).hide();
});


$("div.comment-form").delegate("form", "submit", function() {
	comment = $('#id_comment',this).val();
	submit_url = $('input.submit_url',this).val();
	object_pk = $('input.object_pk',this).val();
	
	wallitemdiv = $(this).parents("div.wallitem");
	
	errordiv = $(wallitemdiv > "div.comment-error")
	errordiv.hide();
	
	$.post(submit_url, {comment: comment,wallitemid: object_pk}, function(data)
	{
		if (data.success) {
				comment_html = '<div id="comment'+ data.commentid  +'" class="comment well deleteable">'+
				'<b>'+data.author+'</b>, <i>'+data.created_at+'  </i>'+data.comment+
				'<div class="delete-button">' +
				'<a id="delete-comment'+ data.commentid +'" href="/wall/deletecomment/'+ data.commentid  +'/"'+
				' class="delete-comment delete-confirm-required">delete</a>'+
				'</div></div>'
				
				commentsdiv=$("div.comments",wallitemdiv);
				commentsdiv.append(comment_html);
		    	commentsdiv.show("slow");

		    	addDeleteConfirm($("#comment"+data.commentid + " a.delete-confirm-required"));
		    	
		    	$("div.comment-form",wallitemdiv).hide();
				
		} else if (data.errors) {
			errors = eval(data.errors);
			errorhtml="";
			$.each(errors,function(fieldname,errmsg)
			{
				errorhtml = errorhtml + errmsg;
			});
		    
		    errordiv_id = "#comment-error" + data.itemid;
		    $(errordiv_id).html(errorhtml);
			$(errordiv_id).show();

		}					

	}, "json");
	return false;
});

