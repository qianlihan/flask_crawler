let member_login_ops = {
  init: function () {
    this.eventBind();
  },
  eventBind: function () {
    $(".login_wrap .do-login").click(function () {
      let btn_target = $(this);
      if (btn_target.hasClass("disabled")) {
        common_ops.alert("Processing");
        return;
      }
      let login_name = $(".login_wrap input[name=login_name]").val();
      let login_pwd = $(".login_wrap input[name=login_pwd]").val();
      if (login_name == undefined || login_name.length < 1) {
        common_ops.alert("Incorrect username");
        return;
      }

      if (login_pwd == undefined || login_pwd.length < 6) {
        common_ops.alert("Incorrect password");
        return;
      }

      btn_target.addClass("disabled");
      $.ajax({
        url: common_ops.buildUrl("/member/login"),
        type: "POST",
        data: {
          login_name: login_name,
          login_pwd: login_pwd,
        },
        dataType: "json",
        success: function (res) {
          btn_target.removeClass("disabled");
          alert(res.msg);
          if (res.code == 200) {
            window.location.href = common_ops.buildUrl("/");
          }
        },
      });
    });
  },
};

$(document).ready(function () {
  member_login_ops.init();
});
