const { default: swal } = require("sweetalert");

//set var
var today = new Date()
var date = today.getFullYear() + "/" + (today.getMonth()+1) + "/" + today.getDate();
var time = today.getHours() + ":" + today.getMinutes();
document.getElementById("date").innerHTML = date;
document.getElementById("time").innerHTML = time;

// $("input[name='date']").attr("value", $.format.date(new Date(), 'yyyy-MM-dd'));
// $("input[name='time']").attr("value", $.format.date(new Date(), 'HH:mm'));

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