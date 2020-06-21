// 此ajax代码为实现局部刷新功能
$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var confirm_pwdE = $("input[name=confirm_pwd]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var confirm_pwd = confirm_pwdE.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        var lgajax = {
            'get':function(args) {
                args['method'] = 'get';
                this.ajax(args);
            },
            'post':function(args) {
                args['method'] = 'post';
                this.ajax(args);
            },
            'ajax':function(args) {
                // 设置csrftoken
                this._ajaxSetup();
                $.ajax(args);
            },
            '_ajaxSetup': function() {
                $.ajaxSetup({
                    'beforeSend':function(xhr,settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                           var csrftoken = $('meta[name=csrf-token]').attr('content');
//                             var csrftoken = $('input[name=csrf-token]').attr('value');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken)
                        }
                    }
                });
            }
        };
        // 接收ResetPasswdView类视图post过来的数据信息，并进行判断输出
        lgajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'confirm_pwd': confirm_pwd
            },
            'success': function (data) {
                // console.log(data);
                // 进行弹窗提示
                if(data['code'] == 200){
                    lgalert.alertSuccess('密码修改成功');
                    // 清空文本框内的密码信息
                    oldpwd.val('');
                    newpwd.val('');
                    confirm_pwd.val('');
                }else{
                    var message = data['message'];
                    lgalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                // console.log(error);
                lgalert.alertNetworkError();
            }
        });
    });
});