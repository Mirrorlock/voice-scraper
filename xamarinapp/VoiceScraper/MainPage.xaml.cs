using CognitiveSpeechService.Services;
using Microsoft.CognitiveServices.Speech;
using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using VoiceScraper.Models;
using Xamarin.Essentials;
using Xamarin.Forms;
using System.Net.Http.Json;
using System.Text;

namespace CognitiveSpeechService
{
    public partial class MainPage : ContentPage
    {
        SpeechRecognizer recognizer;
        IMicrophoneService micService;

        HttpClient client;

        bool isTranscribing = true;

        public MainPage()
        {
            InitializeComponent();
            client = new HttpClient();
            micService = DependencyService.Resolve<IMicrophoneService>();
            InitializeRecognizer();
        }

        private async Task InitializeRecognizer()
        {
            bool isMicEnabled = await micService.GetPermissionAsync();
            if (!isMicEnabled)
            {
                UpdateTranscription("Please grant access to the microphone!");
                return;
            }

            // initialize speech recognizer 
            if (recognizer == null)
            {
                var config = SpeechConfig.FromSubscription(Constants.CognitiveServicesApiKey, Constants.CognitiveServicesRegion);
                recognizer = new SpeechRecognizer(config);
                recognizer.Recognized += async (obj, args) =>
                {
                    string answer = await ProcessSpeech(args.Result.Text);
                    await Speak(answer);
                    UpdateTranscription(args.Result.Text + ":\n" + answer);
                };
            }

            InsertDateTimeRecord();
            await Speak(Constants.GreetString);
        }

        async Task<string> ProcessSpeech(string question)
        {
            var httpContent = new StringContent(JsonSerializer.Serialize(new Question(question)), Encoding.UTF8, "application/json");
            HttpResponseMessage response = await client.PostAsync(Constants.ServerUri, httpContent);
            if (response.IsSuccessStatusCode)
            {
                string content = await response.Content.ReadAsStringAsync();
                Answer answer = JsonSerializer.Deserialize<Answer>(content);
               
                if (answer.Success)
                {
                    return answer.Message;
                }
            }
            return Constants.ResponseErrorString;
        }

        async Task StartListening()
        {
            try
            {
                await recognizer.StartContinuousRecognitionAsync();
                UpdateDisplayState(true);
                isTranscribing = true;
            }
            catch (Exception ex)
            {
                UpdateTranscription(ex.Message);
            }            
        }

        async Task StopListening()
        {
            try
            {
                await recognizer.StopContinuousRecognitionAsync();
                UpdateDisplayState(false);
                isTranscribing = false;
            }
            catch (Exception ex)
            {
                UpdateTranscription(ex.Message);
            }
        }

        async Task Speak(string text)
        {
            if(text != null)
            {
                await StopListening();
                await TextToSpeech.SpeakAsync(text);
                await StartListening();
            }
        }

        async void ChangeState(bool turnOn)
        {
            if (turnOn && !isTranscribing)
            {
                InsertDateTimeRecord();
                await StartListening();
            }
            else if (!turnOn && isTranscribing)
            {
                await StopListening();
            }
        }

        void ChangeStateButton(object sender, EventArgs args)
        {
            ChangeState(!isTranscribing);
        }


        void UpdateTranscription(string newText)
        {
            Device.BeginInvokeOnMainThread(() =>
            {
                if (!string.IsNullOrWhiteSpace(newText))
                {
                    transcribedText.Text += $"{newText}\n";
                }
            });
        }

        void InsertDateTimeRecord()
        {
            Device.BeginInvokeOnMainThread(() =>
            {
                var msg = $"=================\n{DateTime.Now.ToString()}\n=================";
                UpdateTranscription(msg);
            });
        }

        void UpdateDisplayState(bool shouldTranscribe)
        {
            if (!isTranscribing && shouldTranscribe)
            {
                Device.BeginInvokeOnMainThread(() =>
                {
                    transcribeButton.IsEnabled = true;
                    transcribeButton.Text = "Stop";
                    transcribeButton.BackgroundColor = Color.Red;
                    transcribingIndicator.IsRunning = true;
                });
            }
            else if (isTranscribing && !shouldTranscribe)
            {
                Device.BeginInvokeOnMainThread(() =>
                {
                    transcribingIndicator.IsRunning = false;
                    transcribeButton.BackgroundColor = Color.Green;
                    transcribeButton.Text = "Start";
                });
            }
        }
    }
}