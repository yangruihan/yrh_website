$(document).ready(function () {
    // 动态为添加按钮绑定点击事件
    $('body').on('click', '.btn_add_task', function () {
        var button = $(this);
        var num = parseInt(button.attr('id').split('_').pop());
        var content = $('#input_task_content_' + num).val();
        if (content != undefined && content != "") {
            if (button.html() == '增加') {
                $.post("add_task/", {'content': content}, function (data) {
                    if (data != 'fail') {
                        // 修改button显示文字，并记录该任务id号
                        button.html("修改");
                        button.attr("name", data);

                        // 为checkbox、删除button和input记录该任务id号
                        $('#checkbox_task_' + num).attr("name", data);
                        $('#btn_delete_task_' + num).attr("name", data);
                        $('#input_task_content_' + num).attr("name", data);

                        // 添加新任务行
                        next_tr = 
                        '<tr>' + 
                            '<td><input type="checkbox" id="checkbox_task_' + (num + 1) + '" class="checkbox_change_status"></input></td>' + 
                            '<td align="center"><label for="input_task_content_' + (num + 1) + '" id="label_task_' + (num + 1) + '" class="label_task">' + (num + 1) + '</label></td>' +
                            '<td><input type="text" value="" id="input_task_content_' + (num + 1) + '" class="input_task_content"></input></td>' +
                            '<td><button id="btn_add_task_' + (num + 1) + '" class="btn_add_task">增加</button></td>' +
                            '<td><button id="btn_delete_task_' + (num + 1) + '" class="btn_delete_task">删除</button></td>'
                        '</tr>';
                        $('#uncompleted_table').append(next_tr);     
                    }
                });
            } else if (button.html() == '修改') {
                $.post("update_task/", {'id': button.attr('name'), 'content': content}, function (data) {
                    if (data == 'success') {
                        alert("修改成功");
                    } else {
                        alert("修改失败");
                    }
                });
            }
        } else {
            window.location.reload(true);
        }
    });

    // 动态为删除按钮绑定点击事件
    $('body').on('click', '.btn_delete_task', function () {
        var button = $(this);
        if (button.attr('name') != undefined) {
            $.post("delete_task/", {'id': button.attr('name')}, function (data) {
                if (data == 'success') {
                    // alert("删除成功");
                    window.location.reload(true);
                } else {
                    alert("删除失败");
                }
            });
        }
    });

    // 动态为 checkbox 添加状态变化事件
    $('body').on('click', '.checkbox_change_status', function () {
        var checkbox = $(this);
        if (checkbox.is(':checked')) {
            var content = $('#input_task_content_' + checkbox.attr('id').split('_').pop()).val();
            if (content != undefined && content != '') {
                $.post("change_task_status/", {'id': checkbox.attr('name'), 'action': 'finish'}, function (data) {
                    if (data == 'success') {
                        window.location.reload(true);
                    } else {
                        alert("任务完成失败");
                    }
                });
            } else {
                checkbox.removeAttr('checked');
            }
        } else {
            $.post("change_task_status/", {'id': checkbox.attr('name'), 'action': 'unfinish'}, function (data) {
                if (data == 'success') {
                    window.location.reload(true);
                } else {
                    alert("任务重置失败");
                }
            })
        }
    });
    
    var cal = new CalHeatMap();
    var nowDate = new Date();
    cal.init({
    	domain: "month",
    	subDomain: "day",
    	cellSize: 9,
    	range: 12,
    	data: "http://localhost:8000/dailytask/api/get_task_statistics_calendar_data/",
    	cellRadius: 1,
    	domainGutter: 3,
    	displayLegend: true,
    	legend: [1, 2, 4, 8],
    	itemName: ["task", "tasks"],
    	tooltip: true,
    	onClick: function(date, number) {
    		
    	},
    });
});


