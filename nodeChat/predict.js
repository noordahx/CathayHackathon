
const project = 'hack23-team058';
 const location = 'cxhackathon.cathaypacific.com';
const aiplatform = require('@google-cloud/aiplatform');

// Imports the Google Cloud Prediction service client
const {PredictionServiceClient} = aiplatform.v1;

// Import the helper module for converting arbitrary protobuf.Value objects.
const {helpers} = aiplatform;

// Specifies the location of the api endpoint
const clientOptions = {
  apiEndpoint: 'us-central1-aiplatform.googleapis.com',
};
const publisher = 'google';
const model = 'chat-bison@001';

// Instantiates a client
const predictionServiceClient = new PredictionServiceClient(clientOptions);

const predict = async (inputParam) => {
  // Configure the parent resource
  const endpoint = `projects/${project}/locations/${location}/publishers/${publisher}/models/${model}`;

  const prompt = {
    context:
      'My name is Miles. You are an astronomer, knowledgeable about the solar system.',
    examples: [
      {
        input: {content: 'How many moons does Mars have?'},
        output: {
          content: 'The planet Mars has two moons, Phobos and Deimos.',
        },
      },
    ],
    messages: [
      {
        author: 'user',
        content: `${inputParam}`,
      },
    ],
  };
  const instanceValue = helpers.toValue(prompt);
  const instances = [instanceValue];

  const parameter = {
    temperature: 0.2,
    maxOutputTokens: 256,
    topP: 0.95,
    topK: 40,
  };
  const parameters = helpers.toValue(parameter);

  const request = {
    endpoint,
    instances,
    parameters,
  };

  // Predict request
  const [response] = await predictionServiceClient.predict(request);
  console.log('Get chat prompt response');
  const predictions = response.predictions;
  console.log('\tPredictions :');
  for (const prediction of predictions) {
    console.log(`\t\tPrediction : ${JSON.stringify(prediction)}`);
  }

  return { prediction: predictions };
}

module.exports = { predict };