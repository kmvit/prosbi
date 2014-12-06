addLoadEvent(setOver)

function setOver(){
	var light_btns = document.getElementsByClassName('light');
	if (!light_btns) return;
	for (var ii = 0; ii < light_btns.length; ii ++) {
		var cur_img = light_btns[ii];
    		var el, list = cur_img.getElementsByTagName('img');
 		for (var i = 0; i < list.length; i ++) {
  			el = list[i]
  			el.onmouseover = fb1
  			el.onmouseout = fb2
 		}
	}
}

function fb1() {
   var obj = this
   obj.src = obj.src.replace(/\.jpg$/, '_light.jpg')
}

function fb2() {
   var obj = this
   obj.src = obj.src.replace(/\_light\.jpg$/, '.jpg')
}

function addLoadEvent(func) {
	var old = window.onload
	if (typeof window.onload != 'function') window.onload = func
	else window.onload = function() { old(); func(); }
}

// Добавить в Избранное
function add_favorite(a) {
 title=document.title;
 url=document.location;
 try {
   // Internet Explorer
   window.external.AddFavorite(url, title);
 }
 catch (e) {
   try {
     // Mozilla
     window.sidebar.addPanel(title, url, "");
   }
   catch (e) {
     // Opera
     if (typeof(opera)=="object") {
       a.rel="sidebar";
       a.title=title;
       a.url=url;
       return true;
     }
     else {
       // Unknown
       alert('Нажмите Ctrl-D (либо Ctrl+⌘), чтобы добавить страницу в закладки.');
     }
   }
 }
 return false;
}

$(function(){
//Функция увеличивает и уменьшает шрифты на странице
	$('input').click(
		function(){
			var ourText = $('p');
			var currFontSize = ourText.css('fontSize');
			var finalNum = parseFloat(currFontSize, 10);
			var stringEnding = currFontSize.slice(-2);
			if(this.id == 'large') {
				finalNum *= 1.2;
			}
			else if (this.id == 'small'){
				finalNum /=1.2;
			}
			ourText.animate({fontSize: finalNum + stringEnding},600);
	});
});