// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:d16eaa93-4a67-4b85-9f52-00f159f94f1b',
});


var voice_speed = 0;

// x-slow, slow, medium, fast, and x-fast


var is_active = false;

function speakText(text) {
    // Create the JSON parameters for getSynthesizeSpeechUrl

    if (is_active === true) {
        if (voice_speed > 0 || (parseInt(document.cookie) === 1 || parseInt(document.cookie) === 2 || parseInt(document.cookie) === 3 || parseInt(document.cookie) === 4 || parseInt(document.cookie) === 5)) {
            voice_speed = parseInt(document.cookie);

        } else {
            voice_speed = 3;
            document.cookie = voice_speed.toString();
        }

        var rate = "medium";

        if (voice_speed === 3) {
            rate = "medium";
        } else if (voice_speed === 1) {
            rate = "x-slow";
        } else if (voice_speed === 2) {
            rate = "slow";
        } else if (voice_speed === 4) {
            rate = "fast";
        } else if (voice_speed === 5) {
            rate = "x-fast";
        } else if (voice_speed === 6) {
            rate = "175%";
        }


        var speechParams = {
            OutputFormat: "mp3",
            Engine: "neural",
            SampleRate: "16000",
            Text: "<speak><prosody rate='" + rate + "'>" + text + "</prosody></speak>",
            TextType: "ssml",
            VoiceId: "Matthew"
        };


        document.addEventListener('keydown', function (event) {
            if ((event.code === 'ControlLeft' || event.code === 'ControlRight')) {
                // location.reload();
                speakText(" ");
                // unselectSelectedBrush();
            }
        });
        // Create the Polly service object and presigner object


        var polly = new AWS.Polly({apiVersion: '2016-06-10'});
        var signer = new AWS.Polly.Presigner(speechParams, polly)
        // Create presigned URL of synthesized speech file
        signer.getSynthesizeSpeechUrl(speechParams, function (error, url) {
            if (error) {
                console.log("AWS Polly error");
            } else {
                document.getElementById('audioSource').src = url;
                document.getElementById('audioPlayback').load();
                document.getElementById('audioPlayback').play();
            }
        });
    }


}
