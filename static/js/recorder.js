let mic, recorder, soundFile;
let state = 0, start_stopf=false, stop_count = 0;
let bglevel = 0;

$("#start").click(function () {
    start_record();
});

$(document).ready(function(){
    const audio = document.getElementById("player");
    audio.onloadedmetadata = function() {
        console.log('time:', audio.duration);
        setTimeout(start_record, audio.duration * 1000+1000);
        setTimeout(getbglevel, audio.duration * 1000+200);
    };
});

function setup() {
    createCanvas($("#recorder").width()-20,$("#recorder").height()-10).parent("#recorder");

    // create an audio in
    mic = new p5.AudioIn();
    mic.start();

    // create a sound recorder
    recorder = new p5.SoundRecorder();
    recorder.setInput(mic);
    // create a buffer save the recording
    soundFile = new p5.SoundFile();

    // create a frequency spectrum
    fft = new p5.FFT();
    fft.setInput(mic);
}

function getbglevel() {
    var total = 0;
    for(var i = 0; i < 1000; i++) {
        total += mic.getLevel();
    }
    bglevel = total / 1000
    console.log(bglevel);
}

function start_record() {
    stop_count = 0;
    start_stopf = false;
    userStartAudio();
    if (state == 0) {
        state = 1;
        console.log("LISTEN");
    }
}

function stop_record() {
    userStartAudio();
    if (state == 1) {
        if (!start_stopf && mic.getLevel() > bglevel*2) {
            console.log("START");
            recorder.record(soundFile);
            start_stopf = true;
        }

        if (start_stopf && mic.getLevel() < bglevel*2) stop_count += 1;

        if (stop_count > 100) {
            state = 2;
            console.log("STOP");
            recorder.stop();
            setTimeout(save_record, 3000);
        }
        console.log(mic.getLevel(), stop_count);
    }
}

function save_record() {
    userStartAudio();
    if (state == 2) {
        state = 0;
        console.log("SAVE");
        blobToFile(soundFile);
        // soundFile.play();
    }
}
function blobToFile(soundFile) {
    const audioBlob = soundFile.getBlob();
    const formData = new FormData();
    formData.append('audio-file', audioBlob, 'record.wav');

    $.ajax({
        method: "POST",
        url: "http://localhost:5000/audioUpload",
        data: formData,
        processData: false,
        contentType: false,
    })
        .done(function (result) {
            console.log(result);
            if (result["status"] == "success")
                window.location.href = result["url"];
        })
        .fail(function () {
        })
        .always(function () {
        });

}

function draw() {
    background(0, 77, 165);
    let c = color(178, 219, 254);
    fill(c);
    noStroke();
    let spectrum = fft.analyze();
    beginShape();
    
    for (var i = 8; i < spectrum.length/8; i += 20) {
        var x = map(i, 8, spectrum.length/8, 0, width/2)+width/2 - 5;
        var y = map(spectrum[i] * 1.5, 0, 255, height, 0);
        rect(x,0,37,y,0,0);
    }
    for (var i = 8; i < spectrum.length/8; i += 20) {
        var x = width/2-12-15 - map(i, 8, spectrum.length/8, 0, width/2) - 5;
        var y = map(spectrum[i] * 1.5, 0, 255, height, 0);
        rect(x,0,37,y,0,0);
    }

    endShape();
    // console.log(mic.getLevel());
    stop_record();
}