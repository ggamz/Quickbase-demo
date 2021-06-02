using Backend.Models;
using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Data.SQLite;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Dapper;

namespace Backend.CountryDataProviders
{
    public class SqliteDataProvider : ICountryDataProvider
    {
        SQLiteConnection connection;

        public SqliteDataProvider()
        {
            connection = new SQLiteConnection("Data Source=citystatecountry.db;Version=3;FailIfMissing=True");//can be switched to a parameter on demand
        }
        
        public async Task<List<Country>> GetCountries()
        {
            var query = @"
SELECT 
	Country.CountryName AS Name,
	CAST(SUM(IFNULL(City.Population,0)) AS INT) AS Population --Returns double and I can't figure out why
FROM Country
LEFT JOIN State
	ON State.CountryId = Country.CountryId
LEFT JOIN City
	ON City.StateId = State.StateId
GROUP BY Country.CountryName";

            List<Country> res = null;
            try
            {
                connection.Open();
                res = (await connection.QueryAsync<Country>(query)).ToList();
            }
            finally
            {
                if (connection != null)
                {
                    connection.Close();
                }
            }
            return res;
        }
    }
}
