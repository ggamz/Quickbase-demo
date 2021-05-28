using Backend.CountryDataProviders;
using Backend.CountryServices;
using Backend.Loggers;
using Backend.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Backend.PopulationServices
{
    public class RankingCountryService: ICountryService
    {
        private ILogger logger;

        public List<ICountryDataProvider> DataProviders { get; private set; }
        public RankingCountryService(ILogger logger)
        {
            DataProviders = new List<ICountryDataProvider>();
            if (logger == null)
            {
                throw new ArgumentNullException("logger");
            }
            this.logger = logger;
        }

        /// <summary>
        /// Grabs the data for all countries prioritizing sources based on their position in the DataProviders property
        /// </summary>
        /// <returns>Data for all known countries</returns>
        public async Task<List<Country>> GetCountries()
        {
            Dictionary<string, Country> result = new Dictionary<string, Country>();
            List<Country> currentData;
            foreach (var dataProvider in DataProviders.AsEnumerable().Reverse()) 
            {
                //Decided to just log error and not fail completely if datasource fails to return data. Depends on requirements
                try
                {
                    currentData = await dataProvider.GetCountries();
                    if (currentData == null)
                    {
                        throw new Exception(String.Format("DataSource {0} returned null!", dataProvider.GetType()));
                    }
                    //We are depending on the default dictionary behavior, that overwrites previous values and inserts missing ones
                    foreach (var country in currentData)
                    {
                        //relying on names as unique identifiers makes me sad
                        //this should either be switched to ISO 3166 codes if sources allow
                        //or we should use an synonym table, since this way we will have records
                        //that are the same country, but percieved different by the algorithm,
                        //because they are spelled differently
                        result[country.Name] = country;
                    }
                }
                catch (Exception ex)
                {
                    logger.LogError(ex);
                }
            }
            return result.Select(kvp => kvp.Value).ToList();
        }
    }
}
