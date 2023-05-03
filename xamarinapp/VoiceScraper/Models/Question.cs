using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace VoiceScraper.Models
{
    public class Question
    {
        public Question(string text)
        {
            Text = text;
        }

        [JsonPropertyName("text")]
        public string Text
        {
            get;
            set;
        }
    }
}
