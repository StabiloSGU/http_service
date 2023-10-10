function change_sorting_input(e) {
	let header_name = e.target.text;
	let corresponding_input = document.getElementById("sorting_"+header_name);
	switch (corresponding_input.value) {
		case "none":
			console.log('none to asc');
			corresponding_input.setAttribute("value", "asc");
			break;
		case "asc":
			console.log('asc to desc');
			corresponding_input.setAttribute("value", "desc");
			break;
		case "desc":
			console.log('desc to none');
			corresponding_input.setAttribute("value", "none");
			break;
	}
	document.getElementById("filter_and_sort_form").submit()	
}

document.addEventListener('DOMContentLoaded', () => {
	let sort_links = document.getElementsByClassName("sorting")
	for (let link of sort_links) {
		link.addEventListener('click', change_sorting_input);
	}
});