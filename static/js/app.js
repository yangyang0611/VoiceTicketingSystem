// const { default: swal } = require("sweetalert");

// set time
let today, year, month, date, hr, min;
update_time();
setInterval(update_time, 1000*30);
function update_time() {
    today = new Date();
    year = today.getFullYear();
    month = today.getMonth()+1;
    date = today.getDate();
    hr = today.getHours();
    min = today.getMinutes();
    $("#date").text(`${year}/${month}/${date}`);
    $("#time").text(`${hr} : ${min}`);
}

// ##############################
//      select_num.html
// ##############################
function numbtn_click(name){
    console.log("numbtn_click: ",name);
    var index = name.split('_')[1];
    var index_text = $(`button[name='num_${index}']`).text();
    numbtn_css(index);
    window.sessionStorage.setItem("num", index_text);
    console.log("index_text: ",window.sessionStorage.getItem("num"));
}

function numbtn_css(index){
    for(var i = 0; i < 5; i++) {
        $(`button[name='num_${i}']`).removeClass("btn_select_enable");
        if (i == index) $(`button[name='num_${i}']`).addClass("btn_select_enable");
    }
}

// ##############################
//      select_car_time.html
// ##############################

// select time
function time_init() {
    for (var i = 0, m = min, h = hr; i < 20; i++, m+=30){
        if (m >= 60) m-=60, h+=1;
        if (h >= 24) h-=24;
        var button_html = `<button name="time_${i}" type="button" class="btn btn_select_time" onClick="timebtn_click(this.name)">${h.toString().padStart(2,"0")}:${m.toString().padStart(2,"0")}</button>`
        $("#form_time").append(button_html);
    }
}
function timebtn_click(name){
    console.log("timebtn_click: ",index_text);
    var index = name.split('_')[1];
    var index_text = $(`button[name='time_${index}']`).text();
    timebtn_css(index);
    var h = index_text.split(':')[0];
    var m = index_text.split(':')[1];
    window.sessionStorage.setItem("hour", parseInt(h));
    window.sessionStorage.setItem("min", parseInt(m));
    console.log("hour: ",window.sessionStorage.getItem("hour"));
    console.log("min: ",window.sessionStorage.getItem("min"));
}
function timebtn_css(index){
    for(var i = 0; i < 20; i++) {
        $(`button[name='time_${i}']`).removeClass("btn_select_enable");
        if (i == index) $(`button[name='time_${i}']`).addClass("btn_select_enable");
    }
}

// select car
function carbtn_click(name){
    console.log("carbtn_click: ",name);
    var index = name.split('_')[1];
    var index_text = $(`button[name='car_${index}']`).text();
    carbtn_css(index);
    window.sessionStorage.setItem("car", index_text);
    console.log("index_text: ",window.sessionStorage.getItem("car"));
}
function carbtn_css(index){
    for(var i = 0; i < 5; i++) {
        $(`button[name='car_${i}']`).removeClass("btn_select_enable");
        if (i == index) $(`button[name='car_${i}']`).addClass("btn_select_enable");
    }
}

// ##############################
//      select_location.html
// ##############################

// select loc
let city = ["常用","基隆市","新北市","臺北市","桃園市","新竹縣","新竹市","苗栗縣","臺中市","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","臺南市","高雄市","屏東縣","臺東縣","花蓮縣","宜蘭縣"]
let station = {
	"常用": ["基隆","七堵","南港","松山","臺北","萬華","板橋","樹林","桃園","中壢","新竹","竹南","苗栗","豐原","臺中","彰化","員林","斗六","嘉義","新營","臺南","岡山","新左營","高雄","屏東","潮州","臺東","玉里","花蓮","蘇澳新","宜蘭","瑞芳"],
	"基隆市": ["基隆","三坑","八堵","七堵","百福","海科館","暖暖"],
	"新北市": ["五堵","汐止","汐科","板橋","浮洲","樹林","南樹林","山佳","鶯歌","福隆","貢寮","雙溪","牡丹","三貂嶺","大華","十分","望古","嶺腳","平溪","菁桐","猴硐","瑞芳","八斗子","四腳亭"],
	"臺北市": ["南港","松山","臺北","萬華"],
	"桃園市": ["桃園","內壢","中壢","埔心","楊梅","富岡","新富"],
	"新竹縣": ["北湖","湖口","新豐","竹北","竹中","六家","上員","榮華","竹東","橫山","九讚頭","合興","富貴","內灣"],
	"新竹市": ["北新竹","千甲","新莊","新竹","三姓橋","香山"],
	"苗栗縣": ["崎頂","竹南","談文","大山","後龍","龍港","白沙屯","新埔","通霄","苑裡","造橋","豐富","苗栗","南勢","銅鑼","三義"],
	"臺中市": ["日南","大甲","臺中港","清水","沙鹿","龍井","大肚","追分","泰安","后里","豐原","栗林","潭子","頭家厝","松竹","太原","精武","臺中","五權","大慶","烏日","新烏日","成功"],
	"彰化縣": ["彰化","花壇","大村","員林","永靖","社頭","田中","二水","源泉"],
	"南投縣": ["濁水","龍泉","集集","水里","車埕"],
	"雲林縣": ["林內","石榴","斗六","斗南","石龜"],
	"嘉義縣": ["大林","民雄","水上","南靖"],
	"嘉義市": ["嘉北","嘉義"],
	"臺南市": ["後壁","新營","柳營","林鳳營","隆田","拔林","善化","南科","新市","永康","大橋","臺南","保安","仁德","中洲","長榮大學","沙崙"],
	"高雄市": ["大湖","路竹","岡山","橋頭","楠梓","新左營","左營","內惟","美術館","鼓山","三塊厝","高雄","民族","科工館","正義","鳳山","後庄","九曲堂"],
	"屏東縣": ["六塊厝","屏東","歸來","麟洛","西勢","竹田","潮州","崁頂","南州","鎮安","林邊","佳冬","東海","枋寮","加祿","內獅","枋山"],
	"臺東縣": ["大武","瀧溪","金崙","太麻里","知本","康樂","臺東","山里","鹿野","瑞源","瑞和","關山","海端","池上"],
	"花蓮縣": ["富里","東竹","東里","玉里","三民","瑞穗","富源","大富","光復","萬榮","鳳林","南平","林榮新光","豐田","壽豐","平和","志學","吉安","花蓮","北埔","景美","新城","崇德","和仁","和平"],
	"宜蘭縣": ["漢本","武塔","南澳","東澳","永樂","蘇澳","蘇澳新","冬山","羅東","中里","二結","宜蘭","四城","礁溪","頂埔","頭城","外澳","龜山","大溪","大里","石城"],
}
function loc_init() {
    for (var i = 0; i < city.length; i++){
        var button_html = `<div><button name="city_${i}" type="button" class="btn btn_loc" onClick="locbtn_click(this.name)">${city[i]}</button></div>`
        $("#form_loc div[name='city']").append(button_html);
    }
}
function locbtn_click(name){
    console.log("locbtn_click: ",name);
    var index = name.split('_')[1];
    var index_text = $(`button[name='city_${index}']`).text();
    loc_station_generate(index);
    locsbtn_click(`stat_${index}_0`);
    locbtn_css(index);
    console.log("city: ",index_text);
}
function locbtn_css(index){
    for (var i = 0; i < city.length; i++) {
        $(`button[name='city_${i}']`).removeClass("btn_loc_enable");
        if (i == index) $(`button[name='city_${i}']`).addClass("btn_loc_enable");
    }
}
function loc_station_generate(index) {
    var stat = station[city[index]];
    $("#form_loc div[name='station']").html("");
    for (var i = 0; i < stat.length; i++){
        var button_html = `<div><button name="stat_${index}_${i}" type="button" class="btn btn_loc" onClick="locsbtn_click(this.name)">${stat[i]}</button></div>`
        $("#form_loc div[name='station']").append(button_html);
    }
}
function locsbtn_click(name){
    console.log("locsbtn_click: ",name);
    var index_c = name.split('_')[1];
    var index_s = name.split('_')[2];
    var index_text = $(`button[name='${name}']`).text();
    locsbtn_css(index_c, index_s);
    window.sessionStorage.setItem("station", index_text);
    console.log("station: ",window.sessionStorage.getItem("station"));
}
function locsbtn_css(index_c, index_s){
    var stat = station[city[index_c]];
    for (var i = 0; i < stat.length; i++) {
        $(`button[name='stat_${index_c}_${i}']`).removeClass("btn_loc_enable");
        if (i == index_s) $(`button[name='stat_${index_c}_${i}']`).addClass("btn_loc_enable");
    }
}

// pls_come_again.html


// tool
$.fn.serializeForm = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$("button[name='btn_edit_loc']").click(function(){
    Swal.fire({
        title: "警告",
        text: "請問是否要重新輸入目的地？",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: '刪除',
        confirmButtonColor: '#FFEFD8',
        confirmButtonTextColor: 'black',
        cancelButtonText: '取消',
        cancelButtonColor: '#FFB13C'
      })
      .then((result) => {
        if (result.isConfirmed) {
          
        } else {
          
        }
      });
});

$("button[name='btn_edit_num']").click(function(){
    swal({
        title: "警告",
        text: "請問是否要重新輸入張數？",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          
        } else {
          
        }
      });
});

$("button[name='btn_edit_car']").click(function(){
    swal({
        title: "警告",
        text: "請問是否要重新輸入車次？",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          
        } else {
          
        }
      });
});

$("button[name='btn_edit_type']").click(function(){
    swal({
        title: "警告",
        text: "請問是否要重新輸入票種？",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          
        } else {
          
        }
      });
});

$("button[name='btn_cancel_everything']").click(function(){
    swal({
        title: "警告",
        text: "請問是否要取消購票？",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          
        } else {
          
        }
      });
});

$("button[name='second']").click(function(){
    swal("Hi");
});