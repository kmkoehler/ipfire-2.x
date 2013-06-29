function swapVisibility(id) {
	el = document.getElementById(id);
	if(el.style.display != 'block') {
		el.style.display = 'block'
	}
	else 
	{
		el.style.display = 'none'
	}
}