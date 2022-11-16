using GetTvShowTotalLength;
using System.Net.Http.Headers;

class Program
{
    private static async Task<int> Main(string[] args)
    {
        if (args == null || args.Length == 0)
        {
            Environment.Exit(1);
        }
        string query = Convert.ToString(args[0]);
        
        using HttpClient client = new();
        client.DefaultRequestHeaders.Accept.Clear();
        client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));
        APIService service = new(client);

        int id = service.GetShowIdAsync(query).Result;
        List<Show> episodes = await service.GetShowInfoByIdAsync(id);

        int sumRuntime = 0;
        foreach (var episode in episodes ?? Enumerable.Empty<Show>())
        {
            sumRuntime += episode.Runtime ?? 0;
        }
        Console.Write(sumRuntime);
        return 0;
    }
}