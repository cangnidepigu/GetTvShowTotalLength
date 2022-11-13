using System.Text.Json.Serialization;

namespace GetTvShowTotalLength
{
    public record class Show()
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("name")]
        public string? Name { get; set; }

        [JsonPropertyName("runtime")]
        public int? Runtime { get; set; }
    }
}