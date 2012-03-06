$(function() {
  $('#logo').click(function() {
    window.location.href = '/';
  });
  
  $('.exam').hover(function() {
    $(this).addClass('hilight');
  }, function() {
    $(this).removeClass('hilight');
  }).click(function() {
    var $this = $(this);
    var id = $this.attr('id');
	var url = '/getfiles/';
	var params = {
	    folder_id: id
	  }
	$.get(url, params, function(data) {
	  console.log(data);
	  $.each(data, function(k) {
	    $this.append("<div><h3 id='sub'><a href='"+k+"'>" + data[k] + "</a></h3></div>");
	  });
	  //for (var k in data) {
		//$this.append("<div><h3 id='sub'><a href='https://www.box.net/api/1.0/download/8kf9roqysu8jmqskys9vg0hovkmyqtv3/'"+data[k]+">" + k + "</a></h3></div>");
	    //console.log(k + ", " + data[k]);
	  //}
	})
  });
});
