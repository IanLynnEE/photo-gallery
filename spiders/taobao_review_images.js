var review = document.getElementById('J_Reviews');
var control = document.createElement('div');
control.style = 'margin:0px auto;';
control.id = 'review-image-list';
var button = document.createElement('button');
button.innerHTML = 'Get Review Images';
button.style = 'margin:auto; display: block;';
control.appendChild(button);
review.parentNode.insertBefore(control, review.nextSibling);

button.onclick = function() {
    var imgs = review.getElementsByTagName('img');
    for (var i=0; i < imgs.length; ++i) {
		var src = imgs[i].getAttribute('src');
		if (src.length > 10) {
			var p = document.createElement('p');
			p.innerHTML = 'https:' + src;
			control.appendChild(p);
		}
    }
}