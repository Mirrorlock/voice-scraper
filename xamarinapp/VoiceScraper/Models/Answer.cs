using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace VoiceScraper.Models
{
    public class Answer
    {
        [JsonPropertyName("message")]
        public string Message
        {
            get;
            set;
        }

        [JsonPropertyName ("success")]
        public bool Success
        {
            get;
            set;
        }
    }
}
