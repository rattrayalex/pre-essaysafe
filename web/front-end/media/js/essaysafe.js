$(function() {
  $('#logo').click(function() {
    window.location.href = '';
  });
  
  $('.exam').hover(function() {
    $(this).addClass('hilight');
  }, function() {
    $(this).removeClass('hilight');
  }).click(function() {
    var id = $(this).attr('id');
    $.get('https://www.box.net/api/1.0/rest', {
	  action: 'get_account_tree',
	  api_key: 'e74usd65esyarrz614h75i93ik10kku4',
	  auth_token: '8kf9roqysu8jmqskys9vg0hovkmyqtv3',
	  folder_id: id,
	  'params[]':'onelevel',
	  'params[]':'nozip'
	}, function(data) {
	  data = $.parseJSON(data);
	  console.log(data);
	});
  });
});