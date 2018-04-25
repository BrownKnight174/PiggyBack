document.getElementById("loginBtn").onclick = function(){
	$('#loginModal').modal('toggle')
}

function sendData(){
	var url= document.getElementById("sendURL").value;
	if ( url.length == 0)
		alert("Please enter URL");
	else {
	$.post('/home/', url, function(result) {
    alert('successfully posted key1=value1&key2=value2 to foo.php');
});
	}
}

