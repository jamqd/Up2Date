# Houndify JavaScript SDK

The Houndify JavaScript SDK allows you to make voice and text queries to the Houndify API from a web browser or NodeJS. It comes in two forms: 

- the in-browser javascript library [**houndify.js**](https://www.houndify.com/sdks#web) 
- the server-side Node.js module [**houndify**](https://www.npmjs.com/package/houndify). 

Both parts contain functions for sending text and voice requests to the Houndify API. Additionally the in-browser library has an `AudioRecorder` for capturing audio from microphone, and Node.js module has authentication and proxy middleware creators for Express servers.

## Installation
The easiest way to install the SDK is via npm:

```
npm install houndify
```

You can also download the SDK from the [Client SDKs](https://houndify.com/sdks) section of the Houndify website.

## Demo and Examples

### Using JS SDK from the browser
For folks who prefer reading code, there is an `example/` directory in the GitHub repository that shows how to use the SDK with an Express server and an HTML page that accepts voice and text queries, and responds to them. 

To run the demo, download the SDK (see Installation section above). Then follow these steps:

```bash
$ cd /path/to/sdk/example
$ npm install

# Open config.json and add your CLIENT_ID and CLIENT_KEY in.

$ node server.js

# Go to http://localhost:8446 to see the example running. 

# Server-side code is available in server.js
# Client-side code is available in public/index.html
```

### Using JS SDK from NodeJS
You can also use the Houndify JS SDK in a NodeJS environment with no browser at all. To do this, there are two files provided in `example/`:

- node-client-text.js:  Get responses for text requests
- node-client-voice.js: Get responses for audio requests

```bash
# Send a text request from CLI
$ node node-client-text.js --query "what is weather like in New York?"

# Send a voice request from WAV file in CLI
$ node node-client-voice.js --audio ./path/to/audio.wav
```

### Limitations

- **Your browser needs to have access to the microphone**: To accept voice requests, your browser must have the [getUserMedia API](https://caniuse.com/#feat=stream) available. 
- **SSL is required for deployment**: The latest versions of web browsers require secure connection for giving access to microphone. While you can test JavaScript SDK on `localhost` with a HTTP server, you'll need to set up a HTTPS server when you actually deploy it. 
 To do this, set "https" flag in config file to **true**, and point `sslCrtFile` to ssl certificate and `sslKeyFile` to ssl key file. This is only required if you are terminating SSL on the application layer. If deploying with services like Heroku, this will be taken care for you and you don't have to mess with SSL Certificates.




## Setup

### Making Web and Text Requests from the Browser
If you wish to use the JS SDK to send Voice or Text Requests from the browser, you can add a single JS file to your HTML. You can include it via a `<script>` tag and use the global `Houndify` object.

```html
<script src="/path/to/houndify.js"></script>
<script>
const voiceRequest = new Houndify.VoiceRequest({ /* options */ });
</script>
```

You can also *require* `Houndify` as a CommonJS module.

```javascript
const Houndify = require('houndify');
```

However, you still need to add some server-side logic. Specfically, you will need to create a route on your server that will be responsible for sigining the request with your `CLIENT_ID` and `CLIENT_KEY`.


#### Adding Server-side Routes for Signing Requests

The [**houndify**](https://www.npmjs.com/package/houndify) module contains a `HoundifyExpress` object that provides methods to authenticate and proxy voice and text search requests.

The `houndify.HoundifyExpress` object should only be used on the server. It won't work in the browser. It lets you easily create routes to help with:

- Authenticating Requests
- Proxying Text Search Requests

You should setup your NodeJS server with these route handlers because they will be needed when sending requests from the client-side. 


```javascript
var houndifyExpress = require('houndify').HoundifyExpress;

//authenticates requests
app.get('/houndifyAuth', houndifyExpress.createAuthenticationHandler({ 
  clientId:  "YOUR_CLIENT_ID",
  clientKey: "YOUR_CLIENT_KEY"
}));

//proxies text requests
app.post('/textSearchProxy', houndifyExpress.createTextProxyHandler());
```

If your web server is not written in JavaScript, refer to the *Not Using NodeJS* section on how to reimplement these route handlers in other languages.


# Using the SDK


## API Reference

The `Houndify` object following constructors and utility methods. 

* `VoiceRequest(options)` - constructor for initializing voice requests

* `TextRequest(options)` - constructor for initializing text requests

* `AudioRecorder(options)` - constructor for initializing audio recorder for browsers (Chrome, Firefox)

* `decodeAudioData` - utility for decoding audio data uploaded with `FileReader`

* `HoundifyExpress.createAuthenticationHandler` - Express Route Handler for authenticating all Houndify requests through an Express server

* `HoundifyExpress.createTextProxyHandler` - Express Route handler for proxying text requests through an Express server


## Sending Voice Requests with `Houndify.VoiceRequest()`

The `VoiceRequest` constructor allows you to send voice requests between your application and the Houndify backend. It can be used on its own or with an `Houndify.AudioRecorder()` object which will stream recording data directly into it.

The VoiceRequest() constructor takes the following properties:

- `clientId`: Your Client ID
- `clientKey`: Your Client Key
- `authUrl`: The path to the server where the request will get authenticated and signed (See *Adding Server-side Routes for Signing Requests* above)
- `requestInfo`: A valid JSON [RequestInfo](https://docs.houndify.com/reference/RequestInfo) object. 
- `conversationState`: A valid JSON [Conversation State]() object. (See *Supporting Conversation State* section below for more info)
- `sampleRate`: The sample rate of the input audio in Hz (16000 is preferred, 8000 also works)
- `enableVAD`: Boolean specifying whether you want to support Voice Activity Detection (automatically close the mic if it doesn't hear any audio)
- `onTranscriptionUpdate(transcript)`: Function that will be called as partial transcriptions are returned.
- `onResponse(response, info)`: Function that will be called with the final response if the request is successful.
- `onError(error, info): Function that will be called with an error if the request fails.

Here's an example of a sample configuration when instantiating a new `VoiceRequest` object.

```javascript
var voiceRequest = new Houndify.VoiceRequest({
  // Your Houndify Client ID
  clientId: "YOUR_CLIENT_ID",

  // For testing environment you might want to authenticate on frontend without Node.js server. 
  // In that case you may pass in your Houndify Client Key instead of "authURL".
  // clientKey: "YOUR_CLIENT_KEY",

  // Otherwise you need to create an endpoint on your server
  // for handling the authentication.
  // See SDK's server-side method HoundifyExpress.createAuthenticationHandler().
  authURL: "/houndifyAuth",

  // Request Info JSON
  // See https://houndify.com/reference/RequestInfo
  requestInfo: {
    UserID: "test_user",
    Latitude: 37.388309, 
    Longitude: -121.973968
  },

  // Pass the current ConversationState stored from previous queries
  // See https://www.houndify.com/docs#conversation-state
  conversationState: conversationState,

  // Sample rate of input audio
  sampleRate: 16000,
  
  // Convert 8/16 kHz mono 16-bit little-endian PCM samples to Speex, default: true.
  // If set to "false", VoiceRequest.write() will accept raw WAV, Opus or Speex bytes,
  // and send them to backend without any conversion.
  // convertAudioToSpeex: true,

  // Enable Voice Activity Detection, default: true
  enableVAD: true,
  
  // Partial transcript, response and error handlers
  onTranscriptionUpdate: function(transcipt) {
    console.log("Partial Transcript:", transcipt.PartialTranscript);
  },

  onResponse: function(response, info) {
    console.log(response);
    if (response.AllResults && response.AllResults.length) {
      // Pick and store appropriate ConversationState from the results. 
      // This example takes the default one from the first result.
      conversationState = response.AllResults[0].ConversationState;
    }
  },

  onError: function(err, info) {
    console.log(err);
  }
});
```

### VoiceRequest Methods
A `VoiceRequest` object has `write()`, `end()` and `abort()` methods for streaming the audio and ending the request.

```javascript
// By default, VoiceRequest.write() accepts 8/16 kHz mono 16-bit little-endian PCM samples in Int16Array chunks,
// which are converted to Speex format.
// If you want to send raw bytes of WAV, Opus or Speex audio file including header
// set "convertAudioToSpeex" option to false in constructor.
voiceRequest.write(audioChunk);

/* ... */

// Ends streaming voice search requests, expects the final response from backend
voiceRequest.end();

/* ... */

// Aborts voice search request, does not expect final response from backend
voiceRequest.abort();
```

### Best Practices when creating VoiceRequest objects
We recommend creating new `VoiceRequest` objects everytime a new voice request is triggered by the user. There's no need to reuse a single VoiceRequest object.

However, you probably want to keep track of things like the `requestInfo` and `conversationState` objects separately and pass them into each new `VoiceRequest` object that you create.

### Notes about VoiceRequest objects
**Note!** For voice search to work in production the frontend should be served through secure connection. See example project for HTTPS Express server setup. You do not need HTTPS for *localhost*.

You can use Voice Search in the browser without setting up Node.js server. You can pass in the authentication information (Houndify Client ID and Client Key) directly to `HoundifyClient` object and use server of your choice without server-side **houndify** module. **Important!** Your Client Key is private and should not be exposed in the browser in production. Use `VoiceRequest` without server-side authentication only for testing, internal applications or Node.js scripts.

## Recording audio in the browser with Houndify.AudioRecorder()

You can use a `Houndify.AudioRecorder()` object to record audio in Chrome and Firefox and feed it into `VoiceRequest` object. It has *start()*, *stop()*, *isRecording()* methods and accepts handlers for "start", "data", "end" and "error" events.

```javascript
var recorder = new Houndify.AudioRecorder();
var voiceRequest;
recorder.on('start', function() { 
  voiceRequest = new Houndify.VoiceRequest({ ... });
});
recorder.on('data', function(data) {
  voiceRequest.write(data);
 });
recorder.on('end', function() { /* recording stopped, voiceRequest.onResponse() will be called. */ });
recorder.on('error', function(err) { /* recorder error, voiceRequest.onError() will be called. */ });

// Start capturing the audio
recorder.start();

// Stop capturing the audio
recorder.stop();

// Check if recorder is currently capturing the audio
recorder.isRecording();
```

For a better example on how the `AudioRecorder` integrates with the `VoiceRequest` object, view the example inside `/example/public/index.html`.


### Sending Text Requests with Houndify.TextRequest()

The `Houndify.TextRequest()` constructor allows you to send text requests to the Houndify backend and get a JSON response back. It has the following properties: expects query string, Client Id, authentication endpoint/Client Key, request info, conversation state, proxy details and handlers.


- `clientId`: Your Client ID
- `clientKey`: Your Client Key
- `query`: The text query that you want to send to the backend
- `authUrl`: The path to the server where the request will get authenticated and signed (See *Adding Server-side Routes for Signing Requests* above)
- `requestInfo`: A valid JSON [RequestInfo](https://docs.houndify.com/reference/RequestInfo) object. 
- `conversationState`: A valid JSON [Conversation State]() object. (See *Supporting Conversation State* section below for more info)
- `proxy`: A JS object with keys {method, url} that specifies how to proxy the request to the backend. Otherwise, doing this from a front-end file will result in CORS error.
- `onResponse(response, info)`: Function that is called with the response object if the request is successful.
- `onError(error, info)`: Function that is called with an error if the request failed.

Here's an example of a sample `TextRequest` object:

```javascript
var textRequest = new Houndify.TextRequest({
  // Text query
  query: "What is the weather like?",

  // Your Houndify Client ID
  clientId: "YOUR_CLIENT_ID",

  // For testing environment you might want to authenticate on frontend without Node.js server. 
  // In that case you may pass in your Houndify Client Key instead of "authURL".
  // clientKey: "YOUR_CLIENT_KEY",

  // Otherwise you need to create an endpoint on your server
  // for handling the authentication.
  // See SDK's server-side method HoundifyExpress.createAuthenticationHandler().
  authURL: "/houndifyAuth",

  // Request Info JSON
  // See https://houndify.com/reference/RequestInfo
  requestInfo: { 
    UserID: "test_user",
    Latitude: 37.388309, 
    Longitude: -121.973968
  },

  // Pass the current ConversationState stored from previous queries
  // See https://www.houndify.com/docs#conversation-state
  conversationState: conversationState,

  // You need to create an endpoint on your server
  // for handling the authentication and proxying 
  // text search http requests to Houndify backend
  // See SDK's server-side method HoundifyExpress.createTextProxyHandler().
  proxy: {
    method: 'POST',
    url: "/textSearchProxy",
    // headers: {}
    // ... More proxy options will be added as needed
  },
  
  // Response and error handlers
  onResponse: function(response, info) {
    console.log(response);
    if (response.AllResults && response.AllResults.length) {
      // Pick and store appropriate ConversationState from the results. 
      // This example takes the default one from the first result.
      conversationState = response.AllResults[0].ConversationState;
    }
  },

  onError: function(err, info) {
    console.log(err);
  }
});
```

**Note!** In order to use Text Search you'll need a proxy endpoint on your server. `HoundifyExpress` object contains *createTextProxyHandler()* method for setting that up.

### TextRequest Methods
`TextRequest` have no methods available. Once you create them, they will automatically get sent to the server and either `onResponse()` or `onError()` will be called. 

### Best Practices when creating TextRequest objects
Similar to VoiceRequests, you should create a new `TextRequest` object for each text request that the user sends. However, you should keep track of the requestInfo and conversationState objects separately.

## Managing Conversation State
Conversation State is a feature that allows the Houndify backend to know about prior requests made by the user and use that to understand context. For example:

1. "What's the weather in Toronto?"
2. "What about Seattle?" 

This is supported in the SDK via the `conversationState` property that should be set for `Houndify.VoiceRequest` and `Houndify.TextRequest`.

If you want to support Conversation State in your app (you usually will want to), do the following:

1. Define a variable in your application that will manage conversation state for the user. 

```javascript
let userConversationState = {};
```

2. Initially pass in an empty object into the `conversationState` property.

```javascript
let voiceRequest = new Houndify.VoiceRequest({
  ...
  conversationState: userConversationState
})
```

3. In `onReponse()` the Houndify backend will return a new conversation state object, which you should set as the new value of `userConversationState`.

```javascript
let voiceRequest = new Houndify.VoiceRequest({
  ...
  conversationState: userConversationState,
  onResponse: (response, info) => {
    userConversationState = response.AllResults[0].ConversationState;
  }
})
```

4. Now, the conversation state has the prior request in it, and the backend will be able to interpret it on the next `VoiceRequest`.

5. If you ever want to get rid of the conversation state, you can reset it to an empty object.



## Not Using NodeJS?
A NodeJS backend is required if you want to use the JavaScript SDK. If your web server is not written in JavaScript, you can still use the SDK but you will need to re-implement the route handlers for authenticating requests and proxying text requests.

Below, we've added some code to help you do this.

### Reimplementing Authentication Route Handler
**createAuthenticationHandler({ clientId, clientKey })** accepts an object with Houndify Client Id and secret Houndify Client Key and returns an Express handler for authentication requests from client-side `HoundifyClient`. These requests will send a token as a query parameter and expect the signature back as a plain text.

```javascript
var crypto = require('crypto');

/**
 * Given Houndify Client Id and Client Key in options objects
 * returns an Express request handler for authenticating Voice Requests.
 * Signs a token/message with Houndify Client Key using the HMAC scheme.
 * The request for authentications will contain "token" query parameter
 * that needs to be signed with secret Client Key.
 *
 * @param {Object} opts - Options
 * @return {Function} An Express request handler
 */
function createAuthenticationHandler(opts) { 
    return function (req, res) {
        var clientKey = opts.clientKey.replace(/-/g, "+").replace(/_/g, "/");
        var clientKeyBin = new Buffer(clientKey, "base64");
        var hash = crypto.createHmac("sha256", clientKeyBin).update(req.query.token).digest("base64");
        var signature = hash.replace(/\+/g, "-").replace(/\//g, "_");
        res.send(signature);
    }
}
```

### Reimplementing Text Proxy Route Handler
**createTextProxyHandler()** returns a simple Express handler for proxying Text Requests from client-side `HoundifyClient` to Houndify backend. Query parameters of the incoming request should be reused for the request to backend (GET https://api.houndify.com/v1/text). Pick all "hound-*" headers from the incoming request, and send them to the backend with the same names.

```javascript
var request = require('request');

/**
 * Returns a simple Express handler for proxying Text Requests.
 * The handler takes query parameters and houndify headers, 
 * and sends them in the request to backend (GET https://api.houndify.com/v1/text). 
 *
 * @return {Function} An Express request handler
 */
function createTextProxyHandler() {
    return function (req, res) {
        var houndifyHeaders = {};
        for (var key in req.headers) {
            var splitKey = key.toLowerCase().split("-");
            if (splitKey[0] == "hound") {
                var houndHeader = splitKey.map(function(pt) {
                    return pt.charAt(0).toUpperCase() + pt.slice(1);
                }).join("-");
                houndifyHeaders[houndHeader] = req.headers[key];
            }
        }
 
        //GET requests contain Request Info JSON in header.
        //POST requests contain Request Info JSON in body. 
        //Use POST proxy if Request Info JSON is expected to be bigger than header size limit of server
        houndifyHeaders['Hound-Request-Info'] = houndifyHeaders['Hound-Request-Info'] || req.body;

        request({
            url: "https://api.houndify.com/v1/text",
            qs: req.query,
            headers: houndifyHeaders
        }, function (err, resp, body) {
            //if there's an request error respond with 500 and err object
            if (err) return res.status(500).send(err.toString());
            
            //else send the response body from backend as it is
            res.status(resp.statusCode).send(body);
        });  
    }
}
```
