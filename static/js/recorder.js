let mic, recorder, soundFile;
let state = 0, start_stopf=false, stop_count = 0;

$("#start").click(function () {
    start_record();
});

$(document).ready(function(){
    start_record();
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
        if (!start_stopf && mic.getLevel() > 0.001) {
            console.log("START");
            recorder.record(soundFile);
            start_stopf = true;
        }

        if (start_stopf && mic.getLevel() < 0.001) stop_count += 1;

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
    return fetch('http://localhost:5000/audioUpload', {
        method: 'POST',
        body: formData
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