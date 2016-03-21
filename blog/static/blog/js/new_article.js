$(function () {
	// 新建markdown编辑器
	var simplemde = new SimpleMDE({
		element: $("#article_content")[0],
		autoDownloadFontAwesome: true,
		placeholder: "请输入文章内容...",
		hideIcons: ["guide"]
	});
	
	// 为文章分类添加点击事件
	$('body').on('click', '.dropdown-menu li', function (){
		if ($(this).attr('value') != 'new_category') {
			$('#article_category').html($(this).attr('name'));
		}
	});
	
	// 新建分类按钮点击事件
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
	
	// 新建分类 Modal 隐藏事件
	$('#new_category_modal').on('hidden.bs.modal', function (){
		$('#new_category_modal_error_message').hide();
	});
	
	// 新建分类 Modal 显示事件
	$('#new_category_modal').on('show.bs.modal', function (){
		$('#new_category_name').val('');
	});
	
	// 提交按钮点击事件
	$("#btn_submit").click(function () {
		var title = $("#article_title").val();
		if (title == "") {
			$('#new_article_error_message').html("文章名不能为空");
			$('#new_article_error_message').show().delay(4000).fadeOut(3000);
			return;
		}
		
		var category = $("#article_category").html();
		if (category == "" || category == "文章分类") {
			$('#new_article_error_message').html("请选择一个文章分类");
			$('#new_article_error_message').show().delay(4000).fadeOut(3000);
			return;
		} 
		
		$("#category_store").val(category);
		
		var content = simplemde.value();
		
		if (content == "") {
			$('#new_article_error_message').html("请输入文章内容");
			$('#new_article_error_message').show().delay(4000).fadeOut(3000);
			return;
		}
		
		$("#content_store").val(content);
		
		$("#new_article_form").submit();
	});
	
	// 取消按钮点击事件
	$("#btn_cancel").click(function () {
		location.href = "/blog/"
	});
});