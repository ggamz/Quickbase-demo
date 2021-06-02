using Backend.CountryDataProviders;
using Backend.CountryServices;
using Backend.Loggers;
using Backend.PopulationServices;
using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Backend
{
    class Program
    {
        static void Main(string[] args)
        {
            GetCountryData();
        }

        private static async void GetCountryData()
        {
            RankingCountryService svc = new RankingCountryService(new ConsoleLogger());
            svc.DataProviders.Add(new SqliteDataProvider());
            svc.DataProviders.Add(new ConcreteStatDataProvider());
            var res = await svc.GetCountries();
            //Do something with the result
        }
    }
}
