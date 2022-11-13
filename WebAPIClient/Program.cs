using System.Text.Json;
using GetTvShowTotalLength;
using System.Net.Http.Headers;

using HttpClient client = new();
client.DefaultRequestHeaders.Accept.Clear();
client.DefaultRequestHeaders.Accept.Add(
    new MediaTypeWithQualityHeaderValue("application/json"));

List<Show> episodes = await ProcessShowsAsync(client);
int sumRuntime = 0;

foreach (var episode in episodes ?? Enumerable.Empty<Show>())
{
    sumRuntime += episode.Runtime ?? 0;
}


async Task<List<Show>> ProcessShowsAsync(HttpClient client)
{
    if (args == null || args.Length == 0)
    {
        Environment.Exit(1);
    }

    string query = Convert.ToString(args[0]);
    int id = 0;

    // Try to call api to find id of a show
    try
    {
        await using Stream streamId =
            await client.GetStreamAsync($"https://api.tvmaze.com/singlesearch/shows?q={query}");

        var queriedShow =
            await JsonSerializer.DeserializeAsync<Show>(streamId);
        id = queriedShow.Id;
    }
    catch (HttpRequestException)
    {
        Environment.Exit(10);
    }

    // Call api for a list of episodes (using the obtained id)
    await using Stream stream =
        await client.GetStreamAsync($"https://api.tvmaze.com/shows/{id}/episodes");
    var episodes =
        await JsonSerializer.DeserializeAsync<List<Show>>(stream);

    return episodes ?? new();
}

Console.Write(sumRuntime);
return 0;
