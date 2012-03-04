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
	var url = '/getfiles/';
	var params = {
	    folder_id: id
	  }
	$.get(url, params, function(data) {
	  console.log(data);
	})
  });
});