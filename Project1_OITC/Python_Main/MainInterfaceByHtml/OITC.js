getIP()
var my_ip = null;
var page_id = [7, 'page1_main', 'page2_mutigame', 'page3_setting', 'page4_team', 'page5_selfdefine', 'page6_mapchoose', 'page7_serversList'];
var team_id = [3, 'member_intro1', 'member_intro2', 'member_intro3'];
var mem_name = [3, 'pyq', 'hzs', 'zn'];
var character1 = new Array();
var character2 = new Array();
var character3 = new Array();
var frame = 0;
var x = 0;
var y = 0;
var direction = 1;
var loop = 1;
/**********************************************地图显示 */
var map_page_id = [2, 'map_choose_page1', 'map_choose_page2'];
var map_page_queue = ['map_choose_page1', 'map_choose_page2'];
var map_imgs = [5, 'PicAndLogo/skyBg.png', 'PicAndLogo/soilBg.png', 'PicAndLogo/grassBg.png', 'PicAndLogo/stone.png', 'PicAndLogo/desertBg.png'];
var map_names = [5, '天空之城', '初壤之地', '草上之城', '巨石山峰', '大漠对决'];
/**********************************************port列表 */
var port_list = ['7777'];
var is_online = 0;
var is_create = 0;
var room_name = '';
/**********************************************技能选择和技能存储*************/
var chosenSkill = 0;
var time = null;
var distance = null;
var maxVolume = 0;
/***********************************************************/
//显示主界面
showPage(1)
loadImages();
/****************************************开场动画 */
function showAnim() {
	document.getElementById('open_anim').hidden = false;
	document.getElementById('main_body').hidden = true;
}
function hideAnim() {
	document.getElementById('open_anim').style.opacity = 0;
	document.getElementById('main_body').style.opacity = 1;
}
/****************************************动画 */
function loadImages() {
	for (var i = 1; i <= 11; i++) {
		var img = new Image();
		if (i <= 9) {
			img.src = './Character1/p1_walk0' + i + '.png';
		}
		else img.src = './Character1/p1_walk' + i + '.png';
		character1.push(img);
	}
	for (var i = 1; i <= 11; i++) {
		var img = new Image();
		if (i <= 9) {
			img.src = './Character2/p2_walk0' + i + '.png';
		}
		else img.src = './Character2/p2_walk' + i + '.png';
		character2.push(img);
	}
	for (var i = 1; i <= 11; i++) {
		var img = new Image();
		if (i <= 9) {
			img.src = './Character3/p3_walk0' + i + '.png';
		}
		else img.src = './Character3/p3_walk' + i + '.png';
		character3.push(img);
	}
}
function titleAnim() {
	setInterval('float()', 50);
}
function float() {
	var imgs = new Image();
	var canvas = document.getElementById('title_anim');
	var ctx = canvas.getContext('2d');
	var width = canvas.offsetWidth;
	var height = canvas.offsetHeight;
	if (loop == 1) {
		imgs = character1[frame];
		ctx.clearRect(-50, 0, width, height * 1.2);
		ctx.drawImage(imgs, x, y, 15, 45);
		x = x + 1;
		if (x == parseInt(width / 3)) {
			x = 0;
			loop += 1;
			console.log(loop);
		}
		y = y + direction * 1;

		if ((y == 0 || y >= parseInt(Math.floor(Math.random() * height / 1.2))) && y % 5 == 0) {
			direction *= -1;
		}
		if (frame == 10) {
			frame = 0;
		}
		frame++;
		//console.log(imgs);
	}
	else if (loop == 2) {
		imgs = character2[frame];
		ctx.clearRect(-50, 0, width, height * 1.2);
		ctx.drawImage(imgs, x, y, 15, 45);
		x = x + 1;
		if (x == parseInt(width / 3)) {
			x = 0;
			loop += 1;
			console.log(loop);
		}
		y = y + direction * 1;

		if ((y == 0 || y >= parseInt(Math.floor(Math.random() * height / 1.2))) && y % 5 == 0) {
			direction *= -1;
		}
		if (frame == 10) {
			frame = 0;
		}
		frame++;
		//console.log(imgs);
	}
	if (loop == 3) {
		imgs = character3[frame];
		ctx.clearRect(-50, 0, width, height * 1.2);
		ctx.drawImage(imgs, x, y, 15, 45);
		x = x + 1;
		if (x == parseInt(width / 3)) {
			x = 0;
			loop = 1;
			console.log(loop);
		}
		y = y + direction * 1;

		if ((y == 0 || y >= parseInt(Math.floor(Math.random() * height / 1.2))) && y % 5 == 0) {
			direction *= -1;
		}
		if (frame == 10) {
			frame = 0;
		}
		frame++;
		//console.log(imgs);
	}
	//console.log(frame);
}

/**********************************多人游戏界面 */
function hideLoading() {
	document.getElementById('loading').hidden = true;
}
function showLoading() {
	document.getElementById('loading').hidden = false;
}

function runMultiGame() {
	showPage(2);
}
function confirmRoom() {
	room_name = document.getElementById('room_name').value;
	console.log(room_name)
	mapChoose(1);
	cancelRoom();
}
function cancelRoom() {
	//alert('cancel');
	var create_room_box = document.getElementById('create_room');
	create_room_box.style.opacity = 0;
	document.getElementById('mask').hidden = true;
}

function createServer() {
	//alert('Create Server');

	//if (my_ip) {
	//	//alert(my_ip)
	//}
	//else {
	//	alert('Wait for a second')
	//}
	//eel.createServer(my_ip);
	var create_room_box = document.getElementById('create_room');
	create_room_box.style.opacity = 1;
	document.getElementById('mask').hidden = false;
	
}

function joinServer() {
	//alert('Join Server');
	var join_server_box = document.getElementById('join_server');
	join_server_box.style.opacity = 1;
	document.getElementById('mask').hidden = false;

}
function confirmServer() {
	//alert('Confirm');
	var d = distance;
	var duration = time;

	var IP = document.getElementById('IP').value;
	var port = document.getElementById('port').value;
	//alert(IP);
	//alert(port);
	var checkboxes = document.getElementById('is_window');
	var children = checkboxes.childNodes;
	//console.log(children);
	is_window = 1;
	//alert(children[1].checked);
	if (children[1].checked == true)
		is_window = 0;
	//alert(chosenSkill);
	var result = eel.test(is_window, 1, IP.toString(), parseInt(port), 1, chosenSkill, duration, d, my_ip, maxVolume)();
	result.then(ret_val => { if (ret_val == 0) alert('Skill None') });
	//alert('game is over')
}
function cancelServer() {
	//alert('cancel');
	var join_server_box = document.getElementById('join_server');
	join_server_box.style.opacity = 0;
	document.getElementById('mask').hidden = true;
}


//服务器列表显示
function serversList() {
	var result = eel.searchServers(my_ip, port_list)();
	result.then(ret_val => {
		console.log(ret_val);
		var ip_and_port = ret_val[0];//端口
		var map_orders = ret_val[1];
		var room_player_counts = ret_val[2];
		var room_names = ret_val[3];
		console.log(ip_and_port);
		console.log(map_orders);
		console.log(room_player_counts);
		console.log(room_names);
		showPage(7);
		hideLoading();
		var servers_list = document.getElementById('servers_list');
		var content_list = document.getElementsByClassName('serverContent');

		

		for (var i = content_list.length - 1; i >= 0; i--) {
			content_list[i].parentNode.removeChild(content_list[i]);
		}
		for (var i = 0; i < ip_and_port.length; i++) {
			/**增加模块 */
			var target_4 = document.createElement('div');
			target_4.className = "target_4";
			/******************************游戏初始化 */
			var d = distance;
			var duration = time;

			var checkboxes = document.getElementById('is_window');
			var children = checkboxes.childNodes;
			//console.log(children);
			is_window = 1;
			//alert(children[1].checked);
			if (children[1].checked == true)
				is_window = 0;
			var IP = ip_and_port[i][0];
			var port = ip_and_port[i][1];
			/****************************** */
			var content = document.createElement('div');
			content.className = 'serverContent';
			content.dataset.page_id = i;
			content.onclick = function () {
				var result = eel.test(is_window, map_orders[content.dataset.page_id], IP.toString(), parseInt(port), 1, chosenSkill, duration, d, my_ip, maxVolume)();
				result.then(ret_val => { if (ret_val == 0) alert('Skill None') });
			}
			content.onmouseenter = function (e) {
				var map_img = document.getElementById('map_img');
				var map_name = document.getElementById('map_name');
				map_img.src = map_imgs[map_orders[content.dataset.page_id]];
				map_img.style.opacity = 1;
				map_name.innerHTML = map_names[map_orders[content.dataset.page_id]];
			}
			/*content.onmouseover = function (e) {
				var map_img = document.getElementById('map_img');
				var map_name = document.getElementById('map_name');
				map_img.src = map_imgs[map_orders[content.dataset.page_id]];
				map_img.style.opacity = 1;
				map_name.innerHTML = map_names[map_orders[content.dataset.page_id]];
			}*/
			content.onmouseleave = function (e) {
				var map_img = document.getElementById('map_img');
				var map_name = document.getElementById('map_name');
				map_img.style.opacity = 0;
				map_name.innerHTML = '地图介绍';

			}
			//var IP_html = document.createElement('p');
			//var port_html = document.createElement('p');
			//IP_html.innerHTML = IP;
			//port_html.innerHTML = port;
			var room_name_html = document.createElement('p');
			var online_players_html = document.createElement('p');
			room_name_html.innerHTML = '房间名:' + room_names[i];
			online_players_html.innerHTML = '当前在线人数:' + room_player_counts[i];
			content.appendChild(room_name_html);
			content.appendChild(online_players_html);
			servers_list.appendChild(content);
			content.appendChild(target_4)
		}

	})
	showLoading();
}

function getIP() {
	var result = eel.getIP()()
	result.then(ip => document.getElementById("ip").innerHTML = 'IP:' + ip)
	result.then(ip => my_ip = ip)
}
/**********************************主界面 */

function runMyGame(map) {
	var d = distance;
	var duration = time;

	var checkboxes = document.getElementById('is_window');
	var children = checkboxes.childNodes;
	//console.log(children);
	is_window = 1;
	//alert(children[1].checked);
	if (children[1].checked == true)
		is_window = 0;
	//is_window, map = 1, IP = '10.13.87.19', port = 7777, online = 0, skillChosen = 0, time = 0, distance = 0, hostIP = '10.13.87.19'
	eel.test(is_window, map, '10.13.87.19', 0, 0, chosenSkill, duration, d, '10.13.87.19', maxVolume);
}
function setting() {
	showPage(3);
}
function team() {
	showPage(4);
}
function selfdefine() {
	showPage(5);
}

function exit() {
	//eel.exit()
	window.close()
}

/**********************************游戏设置 */

/**********************************制作团队 */
function showIntro(id) {
	for (var i = 1; i <= team_id[0]; i++) {
		if (i == id) {
			//document.getElementById(team_id[i]).hidden = false;
			var mem_id = document.getElementById(team_id[i]);
			mem_id.style.backgroundColor = 'rgba(137, 207, 240,1)';
			document.getElementById(mem_name[i]).style.color = 'rgba(0,0,0,1)';
		}
		else {
			var mem_id = document.getElementById(team_id[i]);
			mem_id.style.backgroundColor = 'rgba(137, 207, 240, 0)';
			document.getElementById(mem_name[i]).style.color = 'rgba(0,0,0,0)';
		}
	}
}
function hideIntro() {
	for (var i = 1; i <= team_id[0]; i++) {
		var mem_id = document.getElementById(team_id[i]);
		mem_id.style.backgroundColor = 'rgba(137, 207, 240, 0)';
		document.getElementById(mem_name[i]).style.color = 'rgba(0,0,0,0)';
	}
}

/**********************************自定义 */
function cancelSkill() {
	document.getElementById('mask2').hidden = true;
	document.getElementById('skills').hidden = true;
	document.getElementById('confirm_skill').hidden = true;
}
function setSkill() {
	document.getElementById('skills').hidden = false;
	document.getElementById('mask2').hidden = false;
	//alert(duration);

}
function record() {
	var result = eel.setSkill()()
	result.then(ret_val => {
		time = ret_val;
		localStorage.setItem('time', time);
		//alert(time);
	})
	result.then(ret_val => eel.confirmSkill(ret_val)().then(ret_val => {
		distance = ret_val[0];
		maxVolume = ret_val[1];
		console.log(ret_val);
		localStorage.setItem('distance', distance);
		localStorage.setItem('maxVolume', maxVolume);
		//alert(distance);
	}))
}
function showSkill(id) {
	document.getElementById('skills_name' + id).style.opacity = 1;
	document.getElementById('skills_intro' + id).style.opacity = 1;
}
function hideSkill(id) {
	document.getElementById('skills_name' + id).style.opacity = 0;
	document.getElementById('skills_intro' + id).style.opacity = 0;
}

function confirmSkill(id) {
	chosenSkill = id;
	localStorage.setItem('chosenSkill', chosenSkill);
	//alert(chosenSkill);
	cancelSkill();
	document.getElementById('mask2').hidden = false;
	document.getElementById('confirm_skill').hidden = false;
}

function cancelConfirmSkill() {
	document.getElementById('skills').hidden = true;
	document.getElementById('confirm_skill').hidden = true;
}
/**********************************通用工具 */
function showPage(id) {
	for (var i = 1; i <= page_id[0]; i++) {
		if (i == id) {
			console.log(page_id[i]);
			document.getElementById(page_id[i]).hidden = false;
		}
		else {
			document.getElementById(page_id[i]).hidden = true;
		}
	}
}
function singleChoice(id) {
	var checkboxes = document.getElementsByName('set_window');
	console.log(checkboxes);
	for (var i = 0; i <= 1; i++) {
		if (id == i)
			checkboxes[i].checked = true;
		else checkboxes[i].checked = false;
	}
}
function backMain() {
	showPage(1);
}
function getStyle(obj, attr) {
	return obj.currentStyle ? obj.currentStyle[attr] : window.getComputedStyle(obj, null)[attr];
}

function animate(obj, json, fn) {
	clearInterval(obj.timer);
	obj.timer = setInterval(function () {
		var bool = true;
		for (var k in json) {
			var leader;
			if (k == 'opacity') {
				if (getStyle(obj, k) == undefined) {
					leader = 100;
				} else {
					leader = parseInt(getStyle(obj, k) * 100);
				}
			} else {
				leader = parseInt(getStyle(obj, k)) || 0;
				//alert(leader);
			}
			//console.log(leader);
			var step = (json[k] - leader) / 10;
			step = step > 0 ? Math.ceil(step) : Math.floor(step);
			leader = leader + step;
			if (k == 'zIndex') {
				obj.style[k] = json[k];
			} else if (k == 'opacity') {
				obj.style[k] = leader / 100;
				obj.style.filter = 'alpha(opacity=' + leader + ')';
			} else {
				obj.style[k] = leader + 'px';
			}
			if (json[k] != leader) {
				bool = false;
			}
		}
		if (bool) {
			clearInterval(obj.timer);
			if (fn) {
				fn();
			}
		}
	}, 10);
}
//不可选中文本
function buildAppInterface() {
	document.body.onselectstart = function () {
		return false;
	}
}
window.onload = function () {
	this.buildAppInterface();
	/****************************添加鼠标事件 */
	this.addMouseEvent();
	/****************************************************开场动画设置 */
	var video = this.document.getElementById('open_anim');
	video.addEventListener("ended", function () {
		video.style.zIndex = -3;
		hideAnim();
	})
	video.addEventListener("click", function () {
		video.muted = !video.muted;
	})
	video.addEventListener("dblclick", function () {
		video.currentTime = 6;
	})
	/****************************************************读取技能缓存 */
	if (this.localStorage.getItem('chosenSkill') && this.localStorage.getItem('time') && this.localStorage.getItem('distance') && this.localStorage.getItem('maxVolume')) {
		this.chosenSkill = parseInt(this.localStorage.getItem('chosenSkill'));
		this.time = parseFloat(this.localStorage.getItem('time'));
		this.distance = parseFloat(this.localStorage.getItem('distance'));
		this.maxVolume = this.parseFloat(this.localStorage.getItem('maxVolume'));
	}
	this.console.log(this.chosenSkill);
	this.console.log(this.time);
	this.console.log(this.distance);
	this.console.log(this.maxVolume);
	/*******************************初始化，隐藏元素*******************/
	this.cancelSkill();
	this.cancelServer();
	this.cancelRoom();
	this.titleAnim();
	this.hideIntro();
	this.hideLoading();
	/********************************设置canvas宽高 */
	var title_wrapper = document.getElementById('title_wrapper');
	var title_width = title_wrapper.offsetWidth;
	var title_height = title_wrapper.offsetHeight;
	var canvas = document.getElementById('title_anim');
	canvas.style.height = 4 * title_height + 'px';
	canvas.style.width = title_width + 'px';
	/********************************设置options最小高度 */
	var mask = document.getElementById('mask');
	var mask2 = document.getElementById('mask2');
	var page1_main = document.getElementById('page1_main');
	var init_height = page1_main.offsetHeight;
	console.log('init_height');
	console.log(init_height);
	for (var i = 1; i <= page_id[0]; i++) {
		var page = document.getElementById(page_id[i]);
		page.setAttribute('data-height', init_height);
	}
	var pages = document.getElementsByClassName('optionsWrapper');
	console.log(pages);
	for (var i = 0; i < page_id[0]; i++) {
		console.log(pages[i].style);
		pages[i].style.minHeight = init_height + 'px';
		console.log(pages[i].style.minHeight);
	}
	/********************************设置mask高 */
	mask.style.height = init_height + 'px';
	mask.style.width = parseInt(title_width - 20) + 'px';
	mask2.style.height = init_height + 'px';
	mask2.style.width = parseInt(title_width - 20) + 'px';
	/********************************设置introduction高 */
	document.getElementById('introduction').style.height = init_height - 90 + 'px';
	//console.log(mask.style.width);
	/********************************设置banner */
	this.banner();
}
/*window.onresize = function () {
	this.banner();
}*/
/********************************设置banner */
function banner() {

	var imgArr = [
		{ "path": "./Banner/4.gif" },
		{ "path": "./Banner/5.gif" },
		{ "path": "./Banner/5.gif" },
		{ "path": "./Banner/4.gif" },
		{ "path": "./Banner/5.gif" }
	];
	var size = [
		{ "top": 20, "left": 10, "width": 20, "height": 60, "zIndex": 1, "opacity": 50 },
		{ "top": 15, "left": 15, "width": 40, "height": 70, "zIndex": 1, "opacity": 70 },
		{ "top": 10, "left": 20, "width": 60, "height": 80, "zIndex": 2, "opacity": 100 },
		{ "top": 15, "left": 45, "width": 40, "height": 70, "zIndex": 1, "opacity": 70 },
		{ "top": 20, "left": 70, "width": 20, "height": 60, "zIndex": 1, "opacity": 50 }
	];
	var imgSum = imgArr.length;
	var wrap = document.getElementById('banner');
	var cont = wrap.firstElementChild || wrap.firstChild;
	var btnArr = wrap.getElementsByTagName('a');
	var flag = true;
	var speed = 7000;
	var height = wrap.offsetHeight;
	var width = wrap.offsetWidth;

	for (var i = 0; i < size.length; i++) {
		size[i].top = parseInt(size[i].top * height * 0.01);
		size[i].left = parseInt(size[i].left * width * 0.01);
		size[i].width = parseInt(size[i].width * width * 0.01);
		size[i].height = parseInt(size[i].height * height * 0.01);
		console.log(size[i]);
	}
	wrap.onmouseover = function () {
		for (var i = 0; i < btnArr.length; i++) {
			btnArr[i].style.display = 'block';
		}
		clearInterval(wrap.timer);
	}
	wrap.onmouseout = function () {
		for (var i = 0; i < btnArr.length; i++) {
			btnArr[i].style.display = 'none';
		}
		wrap.timer = setInterval(function () {
			move(true);
		}, speed);
	}
	for (var i = 0; i < imgSum; i++) {
		var lis = document.createElement('li');
		lis.style.backgroundImage = 'url(' + imgArr[i].path + ')';
		cont.appendChild(lis);
	}
	var liArr = cont.children;
	move();
	wrap.timer = setInterval(function () {
		move(true);
	}, speed);
	btnArr[1].onclick = function () {
		if (flag) {
			move(true);
		}
	}
	btnArr[0].onclick = function () {
		if (flag) {
			move(false);
		}
	}
	function move(bool) {
		if (bool != undefined) {
			if (bool) {
				size.unshift(size.pop());
			} else {
				size.push(size.shift());
			}
		}
		for (var i = 0; i < liArr.length; i++) {
			animate(liArr[i], size[i], function () {
				flag = true;
			});
		}
	}
}

/****************************************************地图翻页*/
//为所有地图页添加鼠标事件
function addMouseEvent() {
	showMapPage();//第一次显示
	for (var i = 1; i <= map_page_id[0]; i++) {
		var page = document.getElementById(map_page_id[i]);
		if (i == 1) {
			page.style.zIndex = 6;
		}
		else {
			page.style.zIndex = 5;
		}
		page.onmousedown = function (e) {
			//console.log(e);
			console.log('down');
		}
		page.onmousemove = function (e) {
			//console.log(e);
			console.log('move');
		}
		page.onmouseup = function (e) {
			//console.log(e);
			console.log('up');
		}
		page.ondblclick = function () {
			var first_page = map_page_queue.shift();
			map_page_queue.push(first_page);
			console.log(map_page_queue);
			showMapPage();
		}
	}
}

function showMapPage() {
	for (var i = 0; i < map_page_queue.length; i++) {
		var page = document.getElementById(map_page_queue[i]);
		if (i == 0) {
			page.style.opacity = 1;
			page.style.zIndex = 6;
		}
		else {
			if (page.style.opacity == 1) {
				page.style.opacity = 0;
			}
			if (page.style.zIndex == 6) {
				page.style.zIndex = 5;
			}
		}
	}
}


/****************************************************地图选择*/
function mapChoose(online) {
	is_online = online;
	showPage(6);
}
/****************************************************开始游戏（多人游戏里的创建游戏以及单人游戏）*/
function runGame(map) {
	if (is_online == 0) {
		runMyGame(map);
	}
	else {
		if (is_create == 0) {
			console.log(room_name);
			console.log(map);
			eel.createServer(my_ip, 7777, map, room_name);
			is_create = 1;
		}
		var d = distance;
		var duration = time;

		var checkboxes = document.getElementById('is_window');
		var children = checkboxes.childNodes;
		//console.log(children);
		is_window = 1;
		//alert(children[1].checked);
		if (children[1].checked == true)
			is_window = 0;

		//showPage(8);
		var result = eel.test(is_window, map, my_ip, 7777, 1, chosenSkill, duration, d, my_ip, maxVolume)();
		result.then(ret_val => { if (ret_val == 0) alert('Skill None') });
	}
}



