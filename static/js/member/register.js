let member_reg_ops = {
  init: function () {
    this.eventBind();
  },
  eventBind: function () {
    $(".reg_wrap .do-reg").click(function () {
      let btn_target = $(this);
      if (btn_target.hasClass("disabled")) {
        common_ops.alert("processing");
        return;
      }
      let nickname = $(".reg_wrap input[name=nickname]").val();
      let login_name = $(".reg_wrap input[name=login_name]").val();
      let login_pwd = $(".reg_wrap input[name=login_pwd1]").val();
      let login_pwd2 = $(".reg_wrap input[name=login_pwd2]").val();
      if (login_name == undefined || login_name.length < 1) {
        common_ops.alert("incorrect username");
        return;
      }

      if (login_pwd == undefined || login_pwd.length < 6) {
        common_ops.alert("Password is too short");
        return;
      }

      if (login_pwd2 == undefined || login_pwd2 != login_pwd) {
        common_ops.alert("Password not matched");
        return;
      }
      if (nickname == undefined) {
        common_ops.alert("Nickname cannot be empty");
        return;
      }
      btn_target.addClass("disabled");
      $.ajax({
        url: common_ops.buildUrl("/member/register"),
        type: "POST",
        data: {
          nickname: nickname,
          login_name: login_name,
          login_pwd: login_pwd,
          login_pwd2: login_pwd2,
        },
        dataType: "json",
        success: function (res) {
          btn_target.removeClass("disabled");
          alert(res.msg);
          if (res.code == 200) {
            //callback = function () {
            window.location.href = common_ops.buildUrl("/member/login");
            //};
          }
        },
      });
    });
  },
};

$(document).ready(() => {
  member_reg_ops.init();
});
