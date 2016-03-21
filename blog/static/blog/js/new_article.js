$(function () {
	var simplemde = new SimpleMDE({
		element: $("#article_content")[0],
		autoDownloadFontAwesome: true,
		placeholder: "请输入文章内容...",
		hideIcons: ["guide"]
	});
	
	$('body').on('click', '.dropdown-menu li', function (){
		if ($(this).attr('value') != 'new_category') {
			$('#article_category').html($(this).attr('name'));
		}
	});
	
	$('#btn_new_category').click(function() {
		var category_name = $('#new_category_name').val();
		if (category_name != "") { 
			$('#new_category_modal').modal('hide');
			$.post('/blog/do_new_category/', {'category_name': category_name}, function (result) {
				if (result == 'fail'){
					$('#new_category_error_message').html("由于系统原因，新建分类失败，给您带来了不便，对此十分抱歉");
					$('#new_category_error_message').show().delay(4000).fadeOut(3000);
				} else if (result == 'exist') {
					$('#new_category_error_message').html("该分类已存在");
					$('#new_category_error_message').show().delay(4000).fadeOut(3000);
				} else {
					str = '<li value="' + result + '" name="' + category_name + '"><a href="#">' + category_name + '</a></li>';
					
					$('#article_category_dropdown').append(str);
					$('#article_category').html(category_name);
					$('#new_category_suc_message').html("分类添加成功");
					$('#new_category_suc_message').show().delay(4000).fadeOut(3000);
				}
			});
		} else {
			$('#new_category_modal_error_message').html("分类名不能为空");
			$('#new_category_modal_error_message').show().delay(4000).fadeOut(3000);
		}
		
	});
	
	$('#new_category_modal').on('hidden.bs.modal', function (){
		$('#new_category_modal_error_message').hide();
	});
	
	$('#new_category_modal').on('show.bs.modal', function (){
		$('#new_category_name').val('')
	});
});