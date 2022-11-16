using System.Net;
using System.Text.Json;

namespace GetTvShowTotalLength
{
    public class APIService
    {
        private readonly HttpClient _client;
        public APIService(HttpClient client) { _client = client; }

        public async Task<List<Show>> GetShowInfoByIdAsync(int id)
        {
            await using Stream stream =
                await _client.GetStreamAsync($"https://api.tvmaze.com/shows/{id}/episodes");
            var episodes =
                await JsonSerializer.DeserializeAsync<List<Show>>(stream);

            return episodes ?? new();
        }

        public async Task<int> GetShowIdAsync(string query)
        {
            int id = 0;
            using HttpResponseMessage response =
                await _client.GetAsync($"https://api.tvmaze.com/singlesearch/shows?q={query}");
            if (response.StatusCode == HttpStatusCode.NotFound)
                Environment.Exit(10);

            try
            {
                await using Stream stream =
                await _client.GetStreamAsync($"https://api.tvmaze.com/singlesearch/shows?q={query}");
                var show =
                    await JsonSerializer.DeserializeAsync<Show>(stream);
                id = show.Id;
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine(e.StackTrace);
                Environment.Exit(1);
            }

            return id;
        }
    }
}
