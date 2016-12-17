$(document).ready(function(){

	$("#button1").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot1');
	});

	$("#button2").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot2');
	});

	$("#button3").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot3');
	});

	$("#button4").click(function(e){
		e.preventDefault();
		load('/test',{}, '#plot4');
	});


	function load(url, data, parent){
		$.ajax({type: "GET",
		  url: url,
		  data: data,
		  success:function(result){
				$(parent).html(result);
		  },
		  error: function (xhr, ajaxOptions, thrownError) {
				$(parent).html('Error, check parameters!: ' + xhr.status + ' ' + thrownError);
			}
		});
	}



});



