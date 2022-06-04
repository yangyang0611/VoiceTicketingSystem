// const { default: swal } = require("sweetalert");

// set time
let today, year, month, date, hr, min;
update_time();
setInterval(update_time, 1000);
function update_time() {
    today = new Date();
    year = today.getFullYear();
    month = today.getMonth()+1;
    date = today.getDate();
    hr = today.getHours();
    min = today.getMinutes();
    $("date").text(`${year}/${month}/${date}`);
    $("time").text(`${hr} : ${min}`);
}

// ##############################
//      select_car_time.html
// ##############################

// select time
function time_init() {
    for (var i = 0, m = min, h = hr; i < 20; i++, m+=30){
        if (m >= 60) m-=60, h+=1;
        if (h >= 24) h-=24;
        var button_html = `<button name="time_${i}" type="button" class="btn_select_time" onClick="timebtn_click(this.name)">${h.toString().padStart(2,"0")}:${m.toString().padStart(2,"0")}</button>`
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
        $(`button[name='time_${i}']`).removeClass("btn_select_car_enable");
        if (i == index) $(`button[name='time_${i}']`).addClass("btn_select_car_enable");
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
        $(`button[name='car_${i}']`).removeClass("btn_select_car_enable");
        if (i == index) $(`button[name='car_${i}']`).addClass("btn_select_car_enable");
    }
}



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

$("button[name='second']").click(function(){
    swal("Hi");
});