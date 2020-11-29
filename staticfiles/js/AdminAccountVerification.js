$("#accept_button").on('click', function () {
      var user_id = $(this).val();
      var is_active = 1;
      console.log(user_id);
      $.ajax({
        url: "{% url 'change_accept_status' %}",
        data: {
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
          'is_active': is_active,
          'user_id': user_id
        },
        dataType: 'json',
        success: function (data) {
          if (data.success) {
            console.log("ajax call success.");
          }else{
            console.log("ajax call not success.");
          }
        }
      });
    });