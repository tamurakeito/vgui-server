//socket.io
var socket = io('http://127.0.0.1:3001', {
    withCredentials: false,
});
socket.on('command', function(msg){
    console.log(msg);
    $('#messages').append($('<li>').text(msg));
});

let audio_sample_rate = null;
let scriptProcessor = null;
let audioContext = null;
let audioData = [];
let bufferSize = 1024;
let second = 1000;

function exportWAV(audioData) {
    let encodeWAV = function (samples, sampleRate) {
        let buffer = new ArrayBuffer(44 + samples.length * 2);
        let view = new DataView(buffer);

        let writeString = function (view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        };

        let floatTo16BitPCM = function (output, offset, input) {
            for (let i = 0; i < input.length; i++ , offset += 2) {
                let s = Math.max(-1, Math.min(1, input[i]));
                output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
            }
        };

        writeString(view, 0, 'RIFF');  // RIFFヘッダ
        view.setUint32(4, 32 + samples.length * 2, true); // これ以降のファイルサイズ
        writeString(view, 8, 'WAVE'); // WAVEヘッダ
        writeString(view, 12, 'fmt '); // fmtチャンク
        view.setUint32(16, 16, true); // fmtチャンクのバイト数
        view.setUint16(20, 1, true); // フォーマットID
        view.setUint16(22, 1, true); // チャンネル数
        view.setUint32(24, sampleRate, true); // サンプリングレート
        view.setUint32(28, sampleRate * 2, true); // データ速度
        view.setUint16(32, 2, true); // ブロックサイズ
        view.setUint16(34, 16, true); // サンプルあたりのビット数
        writeString(view, 36, 'data'); // dataチャンク
        view.setUint32(40, samples.length * 2, true); // 波形データのバイト数
        floatTo16BitPCM(view, 44, samples); // 波形データ

        return view;
    };

    let mergeBuffers = function (audioData) {
        let sampleLength = 0;
        for (let i = 0; i < audioData.length; i++) {
            sampleLength += audioData[i].length;
        }
        let samples = new Float32Array(sampleLength);
        let sampleIdx = 0;
        for (let i = 0; i < audioData.length; i++) {
            for (let j = 0; j < audioData[i].length; j++) {
                samples[sampleIdx] = audioData[i][j];
                sampleIdx++;
            }
        }
        return samples;
    };

    let dataview = encodeWAV(mergeBuffers(audioData), audio_sample_rate);
    let audioBlob = new Blob([dataview], { type: 'audio/wav' });
    console.log(dataview);
    console.log('export complete ...');

    return audioBlob;
};

function sendAudio() {
    var file = exportWAV(audioData);
    upload(file);

    function upload(file){
        var fileReader = new FileReader();
        var send_file = file;
        var data = {};

        fileReader.readAsBinaryString(send_file);
        fileReader.onload = function(event) {
            data.file = event.target.result;
            data.name = "uploadFile";
            console.log('upload file ...');
            socket.emit('upload',data);
        }
        audioData = [];
    }
}

$(function () {
    //録音と送信

    const aryMax = function (a, b) {return Math.max(a, b);}
    const aryMin = function (a, b) {return Math.min(a, b);}

    let recordFlag = false;
    let endFlag = false;
    let judgeFlag = false;

    var onAudioProcess = function (e) {
      var input = e.inputBuffer.getChannelData(0);
      var bufferData = new Float32Array(bufferSize);
      for (var i = 0; i < bufferSize; i++) {
        bufferData[i] = input[i];
      }
      let max = bufferData.reduce(aryMax);
      let min = bufferData.reduce(aryMin);

      if ( recordFlag ) {
        audioData.push(bufferData);
      }else{
        if ( max > 0.5 || min < -0.5 ) {
          recordFlag = true;
          console.log('judge audio...');
          judgeAudio();
        }
      }
    };

    let judgeAudio = function (){
      setTimeout(function () {
        recordFlag = false;
        console.log('send audio...');
        sendAudio();
      }, second);
    }

    let handleSuccess = function (stream) {
      audioContext = new AudioContext({ sampleRate: 16000 });
      //デフォルト値が44100らしい
      audio_sample_rate = audioContext.sampleRate;
      console.log(audio_sample_rate);
      scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1);
      var mediastreamsource = audioContext.createMediaStreamSource(stream);
      mediastreamsource.connect(scriptProcessor);
      scriptProcessor.onaudioprocess = onAudioProcess;
      scriptProcessor.connect(audioContext.destination);

      console.log('record start ...');
    };

    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(handleSuccess);
});
