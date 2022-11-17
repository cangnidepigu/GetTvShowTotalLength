using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.Net.Http.Headers;

namespace GetTvShowTotalLength.Tests
{
    [TestClass()]
    public class APIServiceTests
    {
        [TestMethod()]
        public void GetShowIdAsyncTest_GetsId()
        {
            APIService service = Setup();
            string query = "The Office";

            int id = service.GetShowIdAsync(query).Result;

            Assert.AreEqual(526, id);
        }

        [TestMethod()]
        public async Task GetShowInfoByIdAsync_GetsEpisodes()
        {
            APIService service = Setup();
            int id = 526;
            int totalRuntime = 0;

            List<Show> episodes = await service.GetShowInfoByIdAsync(id);

            Assert.AreNotEqual(0, episodes.Count);
            foreach (var episode in episodes)
            {
                totalRuntime += episode.Runtime ?? 0;
            }
            Assert.AreEqual(6120, totalRuntime);
        }

        private static APIService Setup()
        {
            HttpClient client = new();
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));
            return new APIService(client);
        }
    }
}