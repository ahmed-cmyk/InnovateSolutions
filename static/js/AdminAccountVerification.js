$("#accept_button").on('click', function () {
      var username = $(this).val();
      var active = true;
      console.log(username);
      $.ajax({
        url: 'change_accept_status',
        data: {
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
          'active': active,
          'job_id': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.success) {
            alert("ajax call success.");
            // here you update the HTML to change the active to innactive
          }else{
            alert("ajax call not success.");
          }
        }
      });

    });