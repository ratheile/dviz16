$(document).ready(function(){
  $("#button").click(function(e){
	e.preventDefault();
	$.ajax({type: "GET",
	  url: "/test",
	  data: {},
	  success:function(result){
			$('#plot1').html(result);
	  },
	  error: function (xhr, ajaxOptions, thrownError) {
			$('#status').html('Error, check parameters!: ' + xhr.status + ' ' + thrownError);
		}
	});



	$.ajax({type: "GET",
	  url: "/test",
	  data: {},
	  success:function(result){
			$('#plot2').html(result);
	  },
	  error: function (xhr, ajaxOptions, thrownError) {
			$('#status').html('Error, check parameters!: ' + xhr.status + ' ' + thrownError);
		}
	});
  });
});



