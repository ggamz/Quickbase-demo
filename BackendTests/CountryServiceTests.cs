using Backend.CountryDataProviders;
using Backend.CountryServices;
using Backend.Loggers;
using Backend.Models;
using Backend.PopulationServices;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace BackendTests
{
    [TestClass]
    public class CountryServiceTests
    {
        private Mock<ILogger> GetLogger(StringBuilder sb) 
        {
            var logger = new Mock<ILogger>();
            logger.Setup(log => log.LogError(It.IsAny<string>()))
                .Callback(
                    (string message) => sb.Append(message)
                    ) ;
            logger.Setup(log => log.LogError(It.IsAny<Exception>()))
                .Callback(
                    (Exception exc) => sb.Append(exc.Message)
                    );
            return logger;
        }
        [TestMethod]
        public async Task RankingReturnsFromProperSource()
        {
            var source1 = new Mock<ICountryDataProvider>();
            var source2 = new Mock<ICountryDataProvider>();

            var errors = new StringBuilder();
            var logger = GetLogger(errors);

            var country1 = new Country("Bulgaria", 7000000);
            var country2 = new Country("Bulgaria", 6000000);

            source1.Setup(src => src.GetCountries())
                .Returns(Task.FromResult(new List<Country>() { country1 }));

            source2.Setup(src => src.GetCountries())
                .Returns(Task.FromResult(new List<Country>() { country2 }));


            var service = new RankingCountryService(logger.Object);
            service.DataProviders.Add(source1.Object);
            service.DataProviders.Add(source2.Object);
            var countries = await service.GetCountries();
            Assert.AreEqual(7000000, countries[0].Population);
            Assert.AreEqual("", errors.ToString());
        }

        [TestMethod]
        public async Task RankingReturnsAllCountries()
        {
            var source1 = new Mock<ICountryDataProvider>();
            var source2 = new Mock<ICountryDataProvider>();

            var errors = new StringBuilder();
            var logger = GetLogger(errors);

            var country1 = new Country("Bulgaria", 7000000);
            var country2 = new Country("Bulgaria", 6000000);
            var country3 = new Country("Germany", 80000000);

            source1.Setup(src => src.GetCountries())
                .Returns(Task.FromResult(new List<Country>() { country1 }));

            source2.Setup(src => src.GetCountries())
                .Returns(Task.FromResult(new List<Country>() { country2, country3 }));


            var service = new RankingCountryService(logger.Object);
            service.DataProviders.Add(source1.Object);
            service.DataProviders.Add(source2.Object);
            var countries = await service.GetCountries();
            Assert.AreEqual(2, countries.Count);
            Assert.AreEqual("", errors.ToString());
        }

        [TestMethod]
        public async Task RankingHandlesSourceNotReturningData()
        {
            var source1 = new Mock<ICountryDataProvider>();
            var source2 = new Mock<ICountryDataProvider>();

            var errors = new StringBuilder();
            var logger = GetLogger(errors);

            var country1 = new Country("Bulgaria", 7000000);

            source1.Setup(src => src.GetCountries())
                .Returns(Task.FromResult(new List<Country>() { country1 }));

            source2.Setup(src => src.GetCountries())
                .Returns(Task.FromResult<List<Country>>(null));

            var service = new RankingCountryService(logger.Object);
            service.DataProviders.Add(source1.Object);
            service.DataProviders.Add(source2.Object);

            var countries = await service.GetCountries();

            Assert.AreEqual(1, countries.Count);
            Assert.AreEqual("DataSource Castle.Proxies.ICountryDataProviderProxy returned null!", errors.ToString());
        }

        [TestMethod]
        public async Task RankingHandlesNoSourceReturningData()
        {
            var source1 = new Mock<ICountryDataProvider>();

            var errors = new StringBuilder();
            var logger = GetLogger(errors);

            source1.Setup(src => src.GetCountries())
                .Returns(Task.FromResult<List<Country>>(null));

            var service = new RankingCountryService(logger.Object);
            service.DataProviders.Add(source1.Object);

            var countries = await service.GetCountries();

            Assert.AreEqual(0, countries.Count);
            Assert.AreEqual("DataSource Castle.Proxies.ICountryDataProviderProxy returned null!", errors.ToString());
        }

        [TestMethod]
        public async Task RankingHandlesNoSources()
        {
            var errors = new StringBuilder();
            var logger = GetLogger(errors);

            var service = new RankingCountryService(logger.Object);

            var countries = await service.GetCountries();

            Assert.AreEqual(0, countries.Count);
            Assert.AreEqual("No sources!", errors.ToString());
        }
    }
}
